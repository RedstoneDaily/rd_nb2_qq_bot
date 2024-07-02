from nonebot.adapters.onebot.v11 import MessageSegment
from . import database as db
import nonebot, nonebot.adapters.onebot.v11

# 数据库
permissions = db.get_database('permissions').collection
subscribers = db.get_database('subscribers').collection


class User:
    def __init__(self, id: int):
        if type(id) != int:  # 确保QQ号为整数
            raise TypeError('QQ号必须为整数')
        self.id = id

    @property
    def permission(self) -> int:
        """
        获取用户权限
        """
        return self.get_permission()

    def get_permission(self) -> int:
        """
        获取用户权限
        """

        permission_doc = permissions.find_one({'id': self.id})  # 获取用户权限

        if permission_doc is None:  # 如果用户没有权限，则默认为0
            return 0

        return permission_doc['permission']  # 返回用户权限

    def set_permission(self, permission: int):
        """
        设置用户权限
        :param permission: 权限值
        """

        if type(permission) != int:  # 确保权限值为整数
            raise TypeError('权限值必须为整数')

        permissions.update_one({'id': self.id}, {'$set': {'permission': permission}}, upsert=True)

    def is_subscriber(self) -> bool:
        """
        获取用户订阅状态
        :return: 订阅状态
        """

        sub = subscribers.find_one({'id': str(self.id)})['sub']

        if sub is None:  # 如果用户没有订阅状态，则默认为False
            return False

        return sub  # 返回用户订阅状态

    def set_subscriber(self, sub: bool):
        """
        设置用户订阅状态
        :param sub: 订阅状态
        """

        if type(sub) != bool:  # 确保订阅状态为布尔值
            raise TypeError('订阅状态必须为布尔值')

        subscribers.update_one({'id': str(self.id)}, {'$set': {'sub': sub}}, upsert=True)

    async def send_msg(self, msg: MessageSegment):
        """
         发送私聊消息
         :param msg: 要发送的消息
         """

        await nonebot.get_bot().send_private_msg(user_id=self.id, message=msg)
