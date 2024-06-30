from RedstoneDaily.Plugins.Config import config
from RedstoneDaily.Data import OpreationPermissions
from RedstoneDaily.Utils import turn_message, get_permission, get_args

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message


opreation_permission_matcher = on_command(
    'op', force_whitespace=True, priority=15)
opreation_permission_list_matcher = on_command(
    'op list', force_whitespace=True, priority=10, block=True)
opreation_permission_query_matcher = on_command(
    'op query', force_whitespace=True, priority=10, block=True)
opreation_permission_add_matcher = on_command(
    'op add', force_whitespace=True, priority=10, block=True)
opreation_permission_remove_matcher = on_command(
    'op remove', force_whitespace=True, priority=10, block=True)
opreation_permission_reset_matcher = on_command(
    'op reset', force_whitespace=True, priority=10, block=True)


@opreation_permission_matcher.handle()
async def handle_opreation_permission(event: GroupMessageEvent):
    await opreation_permission_matcher.finish(F'您当前的权限为 {get_permission(event.user_id)} 级。')


@opreation_permission_list_matcher.handle()
async def handle_opreation_permission_list(event: GroupMessageEvent):
    def iterator():
        yield '当前的操作权限列表：'
        for user, permission in OpreationPermissions.data.items():
            yield F'  用户 {user} 的操作权限为 {permission} 级。'
    
    sender_permission = get_permission(event.user_id)
    if sender_permission < 1:
        await opreation_permission_list_matcher.finish('您没有权限执行此操作。')
    message = turn_message(iterator())
    await opreation_permission_list_matcher.finish(message)


@opreation_permission_query_matcher.handle()
async def handle_opreation_permission_query(event: GroupMessageEvent, args: Message = CommandArg()):
    if arg := args.extract_plain_text():
        if not arg.isdigit():
            await opreation_permission_query_matcher.finish('用户 QQ 号格式错误，请重新填写后尝试。')
        await opreation_permission_query_matcher.finish(F'用户 {arg} 的操作权限为 {get_permission(arg)} 级。')
    await opreation_permission_query_matcher.finish('参数不能为空！')


@opreation_permission_add_matcher.handle()
async def handle_opreation_permission_add(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 10:
        await opreation_permission_add_matcher.finish('您没有权限执行此操作。')
    if args := get_args(args):
        if len(args) != 2:
            await opreation_permission_add_matcher.finish('参数错误，请查看语法然后重新尝试。')
        user, permission = args
        if not (user.isdigit() and permission.isdigit()):
            await opreation_permission_add_matcher.finish('用户 QQ 号格式或权限等级格式错误，请重新填写后尝试。')
        permission = int(permission)
        if not 1 <= permission <= 10:
            await opreation_permission_add_matcher.finish('权限等级只能在 1 到 10 之间。')
        OpreationPermissions.data[user] = permission
        await opreation_permission_add_matcher.finish(F'用户 {user} 的操作权限已设置为 {permission} 级。')
    await opreation_permission_add_matcher.finish('参数不能为空')


@opreation_permission_remove_matcher.handle()
async def handle_opreation_permission_remove(event: GroupMessageEvent, args: Message = CommandArg()):
    if get_permission(event.user_id) < 10:
        await opreation_permission_remove_matcher.finish('您没有权限执行此操作。')
    if arg := args.extract_plain_text():
        if not arg.isdigit():
            await opreation_permission_remove_matcher.finish('用户 QQ 号格式错误，请重新填写后尝试。')
        if arg not in OpreationPermissions.data.keys():
            await opreation_permission_remove_matcher.finish(F'用户 {arg} 没有权限，无法删除。')
        OpreationPermissions.data.pop(arg)
    await opreation_permission_remove_matcher.finish('参数不能为空！')


@opreation_permission_reset_matcher.handle()
async def handle_opreation_permission_reset(event: GroupMessageEvent):
    if get_permission(event.user_id) < 10:
        await opreation_permission_reset_matcher.finish(F'您没有权限执行此操作。')
    OpreationPermissions.data = {user: 10 for user in config.superusers}
    await opreation_permission_reset_matcher.finish(F'超级用户的操作权限已重置为 10 级。')
