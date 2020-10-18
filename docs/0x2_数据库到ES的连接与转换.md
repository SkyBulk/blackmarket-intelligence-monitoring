# 数据库到ES的连接与转化

因为项目中使用的爬虫是将数据先存储到MySQL数据库中，在进行下一步搜索、分析操作时，需要将数据库中的表格内容转换到ES中。记录转换到过程。

## 思路

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

## 具体操作

在0x1中，通过电报爬虫，我们获取到了40多万行黑灰产群的message（训练样本文件为`/source/data/telegram_crawler_data.sql`）。

接下来我们需要将该数据库文件做一个简单的清洗和转化，然后把该SQL文件转换为能够存入ES的格式。

### 直接转换SQL文件到ES

