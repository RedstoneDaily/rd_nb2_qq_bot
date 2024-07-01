from redstone_daily.plugins.Config import config
from redstone_daily.Data import OpreationPermissions
from redstone_daily.Utils import turn_message, get_permission, get_args

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, Event

from redstone_daily.plugins.utils import get_context, permission_required

perm_matcher = on_command(
    'op', force_whitespace=True, priority=15)
perm_list_matcher = on_command(
    'op list', force_whitespace=True, priority=10, block=True)
perm_query_matcher = on_command(
    'op query', force_whitespace=True, priority=10, block=True)
perm_add_matcher = on_command(
    'op add', force_whitespace=True, priority=10, block=True)
perm_remove_matcher = on_command(
    'op remove', force_whitespace=True, priority=10, block=True)
perm_reset_matcher = on_command(
    'op reset', force_whitespace=True, priority=10, block=True)


@perm_matcher.handle()
async def handle_opreation_permission(event: Event):
    sender, arg, group = get_context(event)

    await perm_matcher.finish(F'您当前的权限为 {sender.permission} 级。')


@perm_list_matcher.handle()
@permission_required(1)
async def handle_opreation_permission_list(event: GroupMessageEvent):
    sender, arg, group = get_context(event)

    def iterator():  # 操作权限列表迭代器
        yield '当前的操作权限列表：'
        for user, permission in OpreationPermissions.data.items():
            yield F'  用户 {user} 的操作权限为 {permission} 级。'

    message = turn_message(iterator())  # 转换为消息格式
    await perm_list_matcher.finish(message)


@perm_query_matcher.handle()
async def handle_opreation_permission_query(event: GroupMessageEvent, args: Message = CommandArg()):
    if arg := args.extract_plain_text():
        if not arg.isdigit():
            await perm_query_matcher.finish('用户 QQ 号格式错误，请重新填写后尝试。')
        await perm_query_matcher.finish(F'用户 {arg} 的操作权限为 {get_permission(arg)} 级。')
    await perm_query_matcher.finish('参数不能为空！')


@perm_add_matcher.handle()
async def handle_opreation_permission_add(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 10:
        await perm_add_matcher.finish('您没有权限执行此操作。')
    if args := get_args(args):
        if len(args) != 2:
            await perm_add_matcher.finish('参数错误，请查看语法然后重新尝试。')
        user, permission = args
        if not (user.isdigit() and permission.isdigit()):
            await perm_add_matcher.finish('用户 QQ 号格式或权限等级格式错误，请重新填写后尝试。')
        permission = int(permission)
        if not 1 <= permission <= 10:
            await perm_add_matcher.finish('权限等级只能在 1 到 10 之间。')
        OpreationPermissions.data[user] = permission
        await perm_add_matcher.finish(F'用户 {user} 的操作权限已设置为 {permission} 级。')
    await perm_add_matcher.finish('参数不能为空')


@perm_remove_matcher.handle()
async def handle_opreation_permission_remove(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 10:
        await perm_remove_matcher.finish('您没有权限执行此操作。')
    if arg := args.extract_plain_text():
        if not arg.isdigit():
            await perm_remove_matcher.finish('用户 QQ 号格式错误，请重新填写后尝试。')
        if arg not in OpreationPermissions.data.keys():
            await perm_remove_matcher.finish(F'用户 {arg} 没有权限，无法删除。')
        OpreationPermissions.data.pop(arg)
    await perm_remove_matcher.finish('参数不能为空！')


@perm_reset_matcher.handle()
async def handle_opreation_permission_reset(event: GroupMessageEvent):
    if get_permission(event.user_id) < 10:
        await perm_reset_matcher.finish(F'您没有权限执行此操作。')
    OpreationPermissions.data = {user: 10 for user in config.superusers}
    await perm_reset_matcher.finish(F'超级用户的操作权限已重置为 10 级。')
