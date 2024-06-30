from nonebot.adapters.onebot.v11 import Bot

from .user import User
import nonebot


class Group(object):
    def __init__(self, id: int):
        self.id = id

    async def mute(self, user: User, duration_sec: int):
        """
        禁言群成员
        :param user: 被禁言的用户
        :param duration_sec: 禁言时长，单位为秒
        """

        bot = nonebot.get_bot()  # 获取nonebot实例
        await bot.set_group_ban(group_id=self.id, user_id=user.id, duration=duration_sec)

    async def unmute(self, user: User):
        """
        解除群成员禁言
        :param user: 被解除禁言的用户
        """

        bot = nonebot.get_bot()  # 获取nonebot实例
        await bot.set_group_ban(group_id=self.id, user_id=user.id, duration=0)

    async def kick(self, user: User):
        """
        将群成员踢出群
        :param user: 被踢出的用户
        """

        bot = nonebot.get_bot()  # 获取nonebot实例
        await bot.set_group_kick(group_id=self.id, user_id=user.id, reject_add_request=False)

    async def ban(self, user: User):
        """
        将群成员拉黑
        :param user: 被拉黑的用户
        """

        bot = nonebot.get_bot()  # 获取nonebot实例
        await bot.set_group_kick(group_id=self.id, user_id=user.id, reject_add_request=True)

    async def set_nickname(self, user: User, nickname: str):
        """
        设置群成员昵称
        :param user: 要设置昵称的用户
        :param nickname: 昵称
        """

        bot = nonebot.get_bot()  # 获取nonebot实例
        await bot.set_group_card(group_id=self.id, user_id=user.id, card=nickname)