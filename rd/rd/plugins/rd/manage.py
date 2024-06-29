import datetime, time
import json, random

from nonebot.internal.matcher import Matcher
from nonebot.rule import to_me
from nonebot.plugin import *
import requests, nonebot
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot.adapters.onebot.v11 import Event as V11Event, GroupMessageEvent, Bot
from nonebot import require, get_bot
from .utils_old import *

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

mute = on_command('mute')

@mute.handle()
async def handle_mute(bot: Bot, event: GroupMessageEvent):
    """
    禁言命令
    """
    arg = get_args(event)  # 获取命令参数
    sender = event.get_user_id()

    if get_permission(qq = sender) < 80:  # 如果用户等级不足80级，则拒绝执行
        await mute.finish(f'你需要80级以上权限才能执行此命令！你的权限为{get_permission(qq = sender)}')

    if len(arg)!= 2:  # 如果参数个数不为2，则提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    if get_permission(qq = int(arg[0])) >= get_permission(qq = sender):  # 如果被禁言的用户权限高于执行者，则拒绝执行
        await mute.finish('你不能禁言比自己权限高的人！')

    if arg[1].endswith('s'):  # 如果参数以s结尾，则视为秒
        arg[1] = int(arg[1][:-1])
    if arg[1].endswith('m'):  # 如果参数以m结尾，则视为分钟
        arg[1] = int(arg[1][:-1]) * 60
    elif arg[1].endswith('h'):  # 如果参数以h结尾，则视为小时
        arg[1] = int(arg[1][:-1]) * 60 * 60
    elif arg[1].endswith('d'):  # 如果参数以d结尾，则视为天
        arg[1] = int(arg[1][:-1]) * 60 * 60 * 24
    elif arg[1] == '0':  # 如果参数为0，则解除禁言
        arg[1] = 0
    else:  # 提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=int(arg[0]), duration=int(arg[1]))
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await mute.finish('没有权限')

nickname = on_command('set_nickname')

@nickname.handle()
async def handle_nickname(bot: Bot, event: GroupMessageEvent):
    """
    改变群昵称
    """
    arg = get_args(event)  # 获取命令参数
    sender = event.get_user_id()

    if get_permission(qq = sender) < 60:  # 如果用户等级不足60级，则拒绝执行
        await mute.finish(f'你需要60级以上权限才能执行此命令！你的权限为{get_permission(qq = sender)}')

    if len(arg)!= 2:  # 如果参数个数不为2，则提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    if get_permission(qq = int(arg[0])) >= get_permission(qq = sender):  # 如果被改名的用户权限高于执行者，则拒绝执行
        await mute.finish('你不能改名比自己权限高的人！')

    try:
        await bot.set_group_card(group_id=event.group_id, user_id=int(arg[0]), card=arg[1])
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await mute.finish('没有权限')

    await nickname.finish(f'已将{arg[0]}的群昵称改为{arg[1]}')

set_title = on_command('set_title')

@set_title.handle()
async def handle_title(bot: Bot, event: GroupMessageEvent):
    """
    改变群头衔
    """
    arg = get_args(event)  # 获取命令参数
    sender = event.get_user_id()

    if get_permission(qq=sender) < 80:  # 如果用户等级不足80级，则拒绝执行
        await mute.finish(f'你需要80级以上权限才能执行此命令！你的权限为{get_permission(qq=sender)}')

    if len(arg) != 2:  # 如果参数个数不为2，则提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    if get_permission(qq=int(arg[0])) >= get_permission(qq=sender):  # 如果被改头衔的用户权限高于执行者，则拒绝执行
        await mute.finish('你不能更改比自己权限高的人的头衔！')

    try:
        await bot.set_group_special_title(group_id=event.group_id, user_id=int(arg[0]), special_title=arg[1], duration=-1)
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await mute.finish('没有权限')

    await set_title.finish(f'已将{arg[0]}的群头衔改为{arg[1]}')

kick = on_command('kick')

@kick.handle()
async def handle_kick(bot: Bot, event: GroupMessageEvent):
    """
    踢人命令
    """
    arg = get_args(event)  # 获取命令参数
    sender = event.get_user_id()

    if get_permission(qq=sender) < 85:  # 如果用户等级不足85级，则拒绝执行
        await mute.finish(f'你需要85级以上权限才能执行此命令！你的权限为{get_permission(qq=sender)}')

    if len(arg) != 1:  # 如果参数个数不为1，则提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    if get_permission(qq=int(arg[0])) >= get_permission(qq=sender):  # 如果被踢的用户权限高于执行者，则拒绝执行
        await mute.finish('你不能踢比自己权限高的人！')

    try:
        await bot.set_group_kick(group_id=event.group_id, user_id=int(arg[0]), reject_add_request=False)
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await mute.finish('没有权限')

    await set_title.finish(f'已将{arg[0]}踢出群聊')

ban = on_command('ban')

@ban.handle()
async def handle_ban(bot: Bot, event: GroupMessageEvent):
    """
    拉黑
    """
    arg = get_args(event)  # 获取命令参数
    sender = event.get_user_id()

    if get_permission(qq=sender) < 90:  # 如果用户等级不足90级，则拒绝执行
        await mute.finish(f'你需要90级以上权限才能执行此命令！你的权限为{get_permission(qq=sender)}')

    if len(arg) != 1:  # 如果参数个数不为1，则提醒用户输入正确的参数
        await mute.finish('参数错误，请重新输入！')

    if get_permission(qq=int(arg[0])) >= get_permission(qq=sender):  # 如果被拉黑的用户权限高于执行者，则拒绝执行
        await mute.finish('你不能拉黑比自己权限高的人！')

    try:
        await bot.set_group_kick(group_id=event.group_id, user_id=int(arg[0]), reject_add_request=True)
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await mute.finish('没有权限')

    await set_title.finish(f'已将{arg[0]}拉黑')