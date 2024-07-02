from .plugins.Config import config
from .Data import OpreationPermissions

from nonebot.adapters.onebot.v11 import Message, Bot


def get_permission(number: (int | str)):
    number = str(number) if isinstance(number, int) else number
    return OpreationPermissions.data.get(number, 0)


def turn_message(iterator: iter):
    lines = tuple(iterator)
    return Message('\n'.join(lines))


async def broadcast_message(bot: Bot, message: Message):
    for group in config.broadcast_groups:
        await bot.send_group_msg(group_id=group, message=message)
