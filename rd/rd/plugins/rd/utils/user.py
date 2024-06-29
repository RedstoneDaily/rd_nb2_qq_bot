from nonebot.adapters.onebot.v11 import MessageSegment
import database as db
import nonebot

bot = nonebot.get_bot()

# 数据库
permissions = db.get_database('permissions')
subscribers = db.get_database('subscribers')

class User:
    def __init__(self, id):
        if type(self.id) != int:  # 确保QQ号为整数
            raise TypeError('QQ号必须为整数')
        self.id = id

    def get_permission(self) -> int:
        """
        获取用户权限
        """

        return permissions.find_one({'id': self.id})['permission']

    def set_subscriber(self, sub: bool):
        """
        设置用户订阅状态
        :param sub: 订阅状态
        """

        if type(sub) != bool:  # 确保订阅状态为布尔值
            raise TypeError('订阅状态必须为布尔值')

        subscribers.update_one({'id': str(self.id)}, {'$set': {'sub': sub}}, upsert=True)

    def is_subscriber(self) -> bool:
        """
        获取用户订阅状态
        """

        return subscribers.find_one({'id': str(self.id)})['sub']

    def send_msg(self, msg: MessageSegment):
         """
         发送私聊消息
         :param msg: 要发送的消息
         """

         bot.send_private_msg(user_id=self.id, message=msg)