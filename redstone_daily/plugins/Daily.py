from .Config import config
from redstone_daily.Data import Subscribers
from redstone_daily.Utils import turn_message, broadcast_message

import requests
from datetime import datetime, timedelta

from nonebot import get_bot, on_command, require
from nonebot.exception import FinishedException
from nonebot.adapters.onebot.v11 import Event, Bot

from .utils import get_context, get_database, User

require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler


'''
Redstone Daily日报的获取与推送
'''

latest_matcher = on_command('latest', force_whitespace=True)
subscribe_mathcer = on_command('sub', force_whitespace=True)
unsubscribe_matcher = on_command('unsub', force_whitespace=True)

chinese_numbers = ['壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']  # 繁体中文编号


@latest_matcher.handle()
async def latest_daily(bot: Bot):
    ''' 返回最新一期的日报 '''
    try:
        await broadcast_message(bot, '正在获取最新一期的日报，请稍后……')
        message = turn_message(daily_handler())
        await latest_matcher.finish(message)
    except FinishedException:
        pass
    except Exception as error:
        await latest_matcher.finish(F'出错了，请稍后再试！错误信息为 {error}')


@subscribe_mathcer.handle()
async def handle_subscribe(event: Event):
    ''' 订阅日报推送 '''
    sender, arg, group = get_context(event)

    if sender.is_subscriber():
        await subscribe_mathcer.finish('你已经订阅过日报推送了！')  # 已经订阅过
    # 没有订阅过，则添加
    sender.set_subscribe(True)
    await subscribe_mathcer.finish('订阅成功，请加 Bot 好友以接收日报推送！若未添加好友，你将不会收到推送。')


@unsubscribe_matcher.handle()
async def handle_unsubscribe(event: Event):
    ''' 取消日报推送 '''
    sender, arg, group = get_context(event)
    # 确认是否订阅过
    if not sender.is_subscriber():
        await unsubscribe_matcher.finish('你还没有订阅过日报推送！')  # 未订阅过
    # 取消订阅
    sender.set_subscribe(False)
    await unsubscribe_matcher.finish('取消订阅成功！')


def get_data():
    for _ in range(5):
        try:
            response = requests.get('https://redstonedaily.top/api/latest')
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass


def daily_handler():
    '''
    获取最新一期的日报
    :return:
    Message: 最新一期的日报文本
    '''
    if data := get_data():
        # 解析视频
        videos: list = data['content']
        videos.sort(key=lambda info: info['data']['score'], reverse=True)  # 按评分排序
        yield F'最新日报：{data["title"]}'  # 发送消息
        yield '今日前三甲：\n'
        for index, video in enumerate(videos[:3]):
            yield F'{chinese_numbers[index]} 《{video["title"]}》'
            yield (F'  {video["data"]["play"]} / {video["data"]["like"]} / {video["data"]["coin"]} '
                   F'/ {video["data"]["favorite"]} / {video["data"]["share"]} = {round(video["data"]["score"], 2)}\n')
        yield F'更多内容请访问：https://redstonedaily.top/#/daily/{data["title"].replace("-", "/")}'
        return None
    yield '获取日报失败，请稍后再试！运维或者前端来处理一下啊喂 TAT。'


async def everyday_task():
    ''' 每天定时执行一次，推送最新一期的日报 '''
    bot: Bot = get_bot()
    message = turn_message(daily_handler())
    # 向每个推送群发送消息
    await broadcast_message(bot, message)
    # 推送订阅者
    for doc in get_database('subscribers').collection.find():

        user = User(int(doc['id']))
        if doc['sub']:
            # 发送私聊消息
            try:
                await user.send(message)
            except FinishedException:
                pass
            except Exception:
                user.set_subscribe(False)  # 移除出错的订阅者
                message = F'在尝试推送日报给用户 {user.id} 时出错，已移除此订阅者！请加好友后尝试重新订阅。'
                await broadcast_message(bot, message)

hour, minute = config.broadcast_time
next_run_time = (datetime.now() + timedelta(minutes=1))  # 下一次运行时间
paramters = {'next_run_time': next_run_time, 'hour': hour, 'minute': minute}
scheduler.add_job(everyday_task, 'cron', ** paramters)  # 每天在指定的qq时间运行
