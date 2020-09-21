# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class TelegramMessage(Base):
    """
    Telegram的消息类
    用以处理爬虫获取到的Telegram消息的数据，包含以下几个方法：
    - 增加消息
    - 删除消息
    - 修改消息
    - 查询消息
    """

    # 设置对象化表的名字:
    __tablename__ = 'message'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    message_id = Column(String(20))
    chat_id = Column(String(20))
    message = Column(String(1000))
    date = Column(String(20))
    from_id = Column(String(20))
    is_reply = Column(String(20))
    reply_to_msg_id = Column(String(20))
    is_channel = Column(String(20))
    is_group = Column(String(20))
    media_file = Column(String(1000))

    def add_message(self, message_dict):
        """
        方法：增加消息
        """

        # 创建session对象:
        session = DBSession()
        # 创建新User对象:
        for key in message_dict.keys():
            # print(message_dict[key])
            new_message = TelegramMessage(id=message_dict[key][0], message_id=message_dict[key][1], chat_id=message_dict[key][2]
                                          , message=message_dict[key][3], date=message_dict[key][4], from_id=message_dict[key][5])
            # 添加到session:
            session.add(new_message)
            # 提交即保存到数据库:
            session.commit()
        # 关闭session:
        session.close()

    def delete_message_by_id(self, delete_id):
        """
        方法：按ID删除
        """
        session = DBSession()
        # 先查询后删除
        session.query(TelegramMessage).filter(TelegramMessage.id == delete_id).delete()
        session.commit()
        session.close()

    # def delete_message_by_search_item(self, search_item):
    #     """
    #     方法：按消息内容（全部）删除
    #     """
    #     session = DBSession()
    #     # 先查询后删除
    #     item = session.query(TelegramMessage).filter(TelegramMessage.message == search_item).delete()
    #     print(item)
    #     session.commit()
    #     session.close()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:Sz0329..@localhost:3306/telegram')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    """
    测试：增加消息对象
    """
    # message_dict = {}
    # message_dict[0] = ['25083', '400824', '400824', "Hello MySQL", '2020-09-21', '400824']
    #
    # message_obj = TelegramMessage()
    #
    # message_obj.add_message(message_dict=message_dict)

    """
    测试：按ID删除消息
    """
    # message_obj = TelegramMessage()
    # delete_id = '25078'
    # message_obj.delete_message_by_id(delete_id=delete_id)


    """
    测试：按消息内容删除全部消息
    """
#     message_obj = TelegramMessage()
#     delete_message = """
#     新担保交易群
# 全网最全数据库！！！！
# 现在进群，免费送150次查询资格
# 比原机器人更牛逼的来啦
# 新社工裤群：https://t.me/kaifang1
#
# 群讨论频道：https://t.me/dingwei2
#     """
#     message_obj.delete_message_by_search_item(search_item=delete_message)


"""
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message_id` bigint(20) DEFAULT NULL COMMENT '消息ID，同一个群组的消息ID唯一',
  `chat_id` bigint(20) NOT NULL COMMENT '当前对话ID',
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '消息文本',
  `date` datetime(0) DEFAULT NULL,
  `from_id` bigint(20) DEFAULT NULL COMMENT '谁发的',
  `is_reply` tinyint(1) DEFAULT NULL COMMENT '是不是回复某条消息',
  `reply_to_msg_id` bigint(20) DEFAULT NULL COMMENT '回复某条消息的ID',
  `is_channel` tinyint(1) DEFAULT NULL COMMENT '是不是频道',
  `is_group` tinyint(1) DEFAULT NULL COMMENT '是不是群组（频道包括群组）',
  `media_file` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文件路径（比如图片、文件）',
"""
