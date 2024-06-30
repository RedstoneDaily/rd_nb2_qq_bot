from redstone_daily.plugins.Config import config
from redstone_daily.Data import Subscribers
from redstone_daily.Utils import get_permission, turn_message

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message


opreation_permission_subscribe_add_matcher = on_command(
    'op sub add', force_whitespace=True, priority=10, block=True)
opreation_permission_subscribe_list_matcher = on_command(
    'op sub list', force_whitespace=True, priority=10, block=True)
opreation_permission_subscribe_remove_matcher = on_command(
    'op sub remove', force_whitespace=True, priority=10, block=True)
opreation_permission_subscribe_clear_matcher = on_command(
    'op sub clear', force_whitespace=True, priority=10, block=True)


@opreation_permission_subscribe_add_matcher.handle()
async def opreation_permission_subscribe_add(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 5:
        await opreation_permission_subscribe_add_matcher.finish('你没有足够权限执行此操作！')
    if user := args.extract_plain_text():
        if not user.isdigit():
            await opreation_permission_subscribe_add_matcher.finish('输入的 QQ 号格式不正确，请重新输入后尝试！')
        user = int(user)
        if user in Subscribers.data():
            await opreation_permission_subscribe_add_matcher.finish('该用户已经订阅过了，无法重复设置。')
        Subscribers.data.append(user)
        await opreation_permission_subscribe_add_matcher.finish(F'设置用户 {user} 订阅成功！')
    await opreation_permission_subscribe_add_matcher.finish('请输入要订阅的 QQ 号！')


@opreation_permission_subscribe_list_matcher.handle()
async def opreation_permission_subscribe_list(event: GroupMessageEvent):
    def iterator():
        yield '当前订阅用户：'
        for index, user in enumerate(Subscribers.data):
            yield F'({index+1}) {user}'

    if get_permission(event.user_id) < 5:
        await opreation_permission_subscribe_list_matcher.finish('你没有足够权限执行此操作！')
    if Subscribers.data:
        message = turn_message(iterator())
        await opreation_permission_subscribe_list_matcher.finish(message)
    await opreation_permission_subscribe_list_matcher.finish('当前没有任何订阅用户！')


@opreation_permission_subscribe_remove_matcher.handle()
async def opreation_permission_subscribe_remove(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 5:
        await opreation_permission_subscribe_remove_matcher.finish('你没有足够权限执行此操作！')
    if user := args.extract_plain_text():
        if not user.isdigit():
            await opreation_permission_subscribe_remove_matcher.finish('输入的 QQ 号格式不正确，请重新输入后尝试！')
        user = int(user)
        if user not in Subscribers.data:
            await opreation_permission_subscribe_remove_matcher.finish('该用户没有订阅过，无法取消订阅。')
        Subscribers.data.remove(user)
        await opreation_permission_subscribe_remove_matcher.finish(F'取消用户 {user} 订阅成功！')
    await opreation_permission_subscribe_remove_matcher.finish('请输入要取消订阅的 QQ 号！')


@opreation_permission_subscribe_clear_matcher.handle()
async def opreation_permission_subscribe_clear(event: GroupMessageEvent):
    if get_permission(event.user_id) < 10:
        await opreation_permission_subscribe_clear_matcher.finish('你没有足够权限执行此操作！')
    Subscribers.data.clear()
    await opreation_permission_subscribe_clear_matcher.finish('已清空所有订阅用户！')
