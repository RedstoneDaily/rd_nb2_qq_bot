import nonebot
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent

from .user import User


def permission_required(perm: int):
    def decorator(func):
        async def wrapper(event: Event):
            sender = User(event.user_id)
            if sender.get_permission() >= perm:
                return await func(event)
            else:
                bot = nonebot.get_bot()
                if isinstance(event, GroupMessageEvent):
                    await bot.send_group_msg(group_id=event.group_id, message=f'你需要{perm}级权限才能执行此操作')
                else:
                    await sender.send_msg(f'你需要{perm}级权限才能执行此操作')

        return wrapper

    return decorator
