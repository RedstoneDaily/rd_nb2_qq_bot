from user import User
import nonebot

bot = nonebot.get_bot()  # 获取nonebot实例

class Group(object):
    def __init__(self, id):
        self.id = id

    def mute(self, user: User, duration_min: int):
        """
        禁言群成员
        :param user: 被禁言的用户
        :param duration_min: 禁言时长，单位为分钟
        """

        bot.set_group_ban(self.id, user.id, duration_min * 60)

    def unmute(self, user: User):
        """
        解除群成员禁言
        :param user: 被解除禁言的用户
        """

        bot.set_group_ban(self.id, user.id, 0)

    def kick(self, user: User):
        """
        将群成员踢出群
        :param user: 被踢出的用户
        """

        bot.set_group_kick(self.id, user.id, False)

    def ban(self, user: User):
        """
        将群成员拉黑
        :param user: 被拉黑的用户
        """

        bot.set_group_kick(self.id, user.id, True)

    def set_nickname(self, user: User, nickname: str):
        """
        设置群成员昵称
        :param user: 要设置昵称的用户
        :param nickname: 昵称
        """

        bot.set_group_card(self.id, user.id, nickname)