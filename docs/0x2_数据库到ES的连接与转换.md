# 数据库到ES的连接与转化

因为项目中使用的爬虫是将数据先存储到MySQL数据库中，在进行下一步搜索、分析操作时，需要将数据库中的表格内容转换到ES中。记录转换到过程。

## 0. 思路

-   使用logstash进行
    -   使用插件logstash-input-jdbc
    -   参考：https://zhuanlan.zhihu.com/p/40177683
-   使用消息队列
    -   参考：https://blog.csdn.net/weixin_38399962/article/details/107918244
-   使用go-mysql-elasticsearch插件
    -   参考：https://my.oschina.net/u/4000872/blog/2252620
-   Apache-NiFi实现mysql数据与elasticsearch同步
    -   参考：https://my.oschina.net/u/4000872/blog/2252620
-   使用DataX
    -   项目：https://github.com/alibaba/DataX
-   基于MySQL Binlog
    -   参考：https://dbaplus.cn/news-11-2722-1.html

## 1. 具体操作

在0x1中，通过电报爬虫，我们获取到了40多万行黑灰产群的message（训练样本文件为`/source/data/telegram_crawler_data.sql`）。

接下来我们需要将该数据库文件做一个简单的清洗和转化，然后把该SQL文件转换为能够存入ES的格式。

### 1.1 使用logstash进行

使用logstash和JDBC同步MySQL数据到ES。原理是通过logstash支持的两个插件：`logstash-input-jdbc`和`logstash-output-elasticsearch`。原理就是通过`logstash-input-jdbc`，利用JDBC读取MySQL中的数据，输入到logstah。然后通过`logstash-output-elasticsearch`插件从logstash中输出数据到ES。

参考：

-   https://juejin.im/post/6844903858070618126
-   https://segmentfault.com/a/1190000014387486

#### 1.1.1 部署logstash

测试环境使用HomeBrew安装：

```bash
$ brew install logstash
```

#### 1.1.2 安装插件

使用logstash和JDBC同步MySQL数据到ES，需要让logstash安装关于JDBC和ES的插件：`logstash-input-jdbc`和`logstash-output-elasticsearch`。但在新版本的logstash中，以上插件均已集成。

```bash
$ logstash-plugin install logstash-input-jdbc
$ logstash-plugin install logstash-output-elasticsearch
```

#### 1.1.3 下载JDBC驱动

JDBC下载：https://dev.mysql.com/downloads/connector/j/

测试环境为macOS，所以选择Platform Independent，下载压缩包，解压，获得其中的jar包即可。

#### 1.1.4 编写配置文件

现在来编写logstash的配置文件，使用HomeBrew安装的目录地址为：`/usr/local/Cellar/logstash/7.9.1/libexec/config/logstash-sample.conf`。编辑此文件，最好先做个备份。以下是配置文件的编写示例：

```yaml
# Sample Logstash configuration for creating a simple
# Beats -> Logstash -> Elasticsearch pipeline.

input {
  jdbc{
    # mysql 数据库链接
    # jdbc_connection_string => "jdbc:mysql:192.168.177.128:3306/test_datax_1?characterEncoding=utf8"
    jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/telegram?useUnicode=true&characterEncoding=utf-8&useSSL=false"
    # 用户名和密码
    jdbc_user => "root"
    jdbc_password => "YourPassword"
    #驱动
    jdbc_driver_library => "/YourFilePath2JDBC/jdbc/mysql-connector-java-8.0.22.jar"
    # 驱动类名
    jdbc_driver_class => "com.mysql.jdbc.Driver"
    jdbc_paging_enabled => "true"
    jdbc_page_size => "50000"
    jdbc_default_timezone =>"Asia/Shanghai"
    # mysql文件, 也可以直接写SQL语句在此处，后面会把读取到的全部数据都发送出去：
    statement => "select * from message"
    # statement_filepath => "./config/jdbc.sql"
    # 这里类似crontab,可以定制定时操作，比如每分钟执行一次同步(分 时 天 月 年)
    schedule => "* * * * *"
    type => "jdbc"
    # 是否记录上次执行结果, 如果为真,将会把上次执行到的 tracking_column 字段的值记录下来,保存到 last_run_metadata_path 指定的文件中
    #record_last_run => true
    # 是否需要记录某个column 的值,如果record_last_run为真,可以自定义我们需要 track 的 column 名称，此时该参数就要为 true. 否则默认 track 的是 timestamp 的值.
    # use_column_value => true
    # 如果 use_column_value 为真,需配置此参数. track 的数据库 column 名,该 column 必须是递增的. 一般是mysql主键
    # tracking_column => "update_time"
    # tracking_column_type => "timestamp"
    # last_run_metadata_path => "./logstash_capital_bill_last_id"
    # 是否清除 last_run_metadata_path 的记录,如果为真那么每次都相当于从头开始查询所有的数据库记录
    # clean_run => false
    # 是否将 字段(column) 名称转小写
    lowercase_column_names => false
  }
}

output {
 elasticsearch {
   hosts => ["http://localhost:9200"]
  #  index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
   # 输出的索引名称
   index => telegram_message_0x0
   # user => "elastic"
   # password => "changeme"
 } 
 # 屏幕输出，供测试使用，可以不显示
 stdout {
     codec => json_lines
     }   
}
```

#### 1.1.5 运行logstash

接下来我们使用`-f`命令指定配置文件，即可启动logstash：

```bash
$ logstash -f my-logstash.conf
```

#### 1.1.6 查询ES

最后，我们发送请求到ES，看是否存入到指定的索引中：

```http
GET http://127.0.0.1:9200/_cat/indices?pretty=true
```