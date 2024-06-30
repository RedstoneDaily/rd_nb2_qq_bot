import nonebot
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent

from .user import User


def permission_required(perm: int):
    """
    权限检查装饰器
    :param perm: 权限等级
    :return: 装饰器
    """
    def decorator(func):
        async def wrapper(event: Event, *args, **kwargs):
            sender = User(event.user_id)   # 获取用户信息
            if sender.get_permission() >= perm:  # 判断用户权限是否满足要求
                return await func(event, *args, **kwargs)  # 执行函数
            else:   # 权限不足
                bot = nonebot.get_bot()
                if isinstance(event, GroupMessageEvent):
                    await bot.send_group_msg(group_id=event.group_id, message=f'你需要{perm}级权限才能执行此操作')  # 发送权限不足消息
                else:
                    await sender.send_msg(f'你需要{perm}级权限才能执行此操作')

        return wrapper

    return decorator
