import json
from nonebot.plugin import *
import requests, nonebot
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot.adapters.onebot.v11 import Event as V11Event, GroupMessageEvent, Bot
from nonebot import require

from . import utils

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

"""
Redstone Daily日报的获取与推送
"""


def get_daily():
    """
    获取最新一期的日报
    :return:
    str: 最新一期的日报文本
    """

    def get_data(retry=0):
        if retry > 5:  # 重试5次
            raise Exception("获取数据失败")
        try:  # 获取最新一期的日报
            response = requests.get("https://redstonedaily.top/api/latest")
            data = response.json()
            return data
        except:  # 出错则重试
            return get_data(retry + 1)

    data = get_data()

    # 解析视频
    videos = data["content"]
    videos.sort(key=lambda x: x["data"]["score"], reverse=True)  # 按评分排序

    log = f"最新日报: {data['title']}\n"  # 发送消息
    head = (f"今日前三甲: \n\n壹 {videos[0]['title']}\n{videos[0]['data']['play']} / {videos[0]['data']['like']} / "
            f"{videos[0]['data']['coin']} / {videos[0]['data']['favorite']} / {videos[0]['data']['share']} = {round(videos[0]['data']['score'], 2)}\n\n") if len(
        videos) >= 1 else ""
    second = (f"贰 {videos[1]['title']}\n{videos[1]['data']['play']} / {videos[1]['data']['like']} / "
              f"{videos[1]['data']['coin']} / {videos[1]['data']['favorite']} / {videos[1]['data']['share']} = {round(videos[1]['data']['score'], 2)}\n\n") if len(
        videos) >= 2 else ""
    third = (f"叁 {videos[2]['title']}\n{videos[2]['data']['play']} / {videos[2]['data']['like']} / "
             f"{videos[2]['data']['coin']} / {videos[2]['data']['favorite']} / {videos[2]['data']['share']} = {round(videos[2]['data']['score'], 2)}\n\n") if len(
        videos) >= 3 else ""
    link = f"更多内容请访问：https://redstonedaily.top/#/daily/{data['title'].split('-')[0]}/{data['title'].split('-')[1]}/{data['title'].split('-')[2]}"

    return log + head + second + third + link


async def run_every_day():
    """
    每天16:30执行一次
    发送最新一期的日报
    """
    data_file = store.get_data_file("rd", "subscribe.json")
    subscribe_data = data_file.read_text()
    subscribers = json.loads(subscribe_data)

    # 发送消息
    bot = nonebot.get_bot()

    try:  # 尝试获取日报
        news = get_daily()
    except Exception:  # 获取失败
        news = "获取日报失败，运维或者前端来处理一下啊喂 TAT。"
        await bot.send_group_msg(group_id=291728287, message=news)

    await bot.send_group_msg(group_id=291728287, message=news)
    for qq_number in subscribers:
        # 发送私聊消息
        try:
            await bot.send_private_msg(user_id=int(qq_number), message=news)
        except:
            subscribers.remove(qq_number)  # 移除出错的订阅者
            data_file.write_text(json.dumps(subscribers))  # 存储订阅者列表
            await bot.send_group_msg(group_id=291728287,
                                     message=f"在尝试推送日报给{qq_number}时出错，已移除订阅者。请重新订阅。")


latest = on_command("latest")


@latest.handle()
async def newest_daily():
    """
    返回最新一期的日报
    """
    try:
        await latest.finish(get_daily())
    except nonebot.exception.FinishedException:
        pass
    except Exception as e:
        await latest.finish(f"出错了，请稍后再试。\n{e}")


subscribe = on_command("sub")


@subscribe.handle()
async def subscribe_daily(event: Event):
    """
    订阅日报推送
    """
    # 获取qq号
    qq_number = event.user_id

    # 存储qq号
    try:
        # 读取数据文件
        data_file = store.get_data_file("rd", "subscribe.json")
        subscribe_data = data_file.read_text()
    except:
        # 如果数据为空，则初始化
        subscribe_data = '[]'
        data_file.write_text(subscribe_data)

    # 存储qq号
    subscribers = json.loads(subscribe_data)

    if qq_number in subscribers:
        await subscribe.finish("你已经订阅过日报推送了！")  # 已经订阅过

    # 没有订阅过，则添加
    subscribers.append(qq_number)
    data_file.write_text(json.dumps(subscribers))

    await subscribe.finish("订阅成功！请加bot好友以接收日报推送！（这是必须的要求）可以加群291728287获取通知")


unsubscribe = on_command("unsub")


@unsubscribe.handle()
async def unsubscribe_daily(event: Event):
    """
    取消日报推送
    """
    # 获取qq号
    qq_number = event.user_id

    try:
        # 读取数据文件
        data_file = store.get_data_file("rd", "subscribe.json")
        subscribe_data = data_file.read_text()

        # 存储qq号
        subscribers = json.loads(subscribe_data)
        subscribers.remove(qq_number)
        data_file.write_text(json.dumps(subscribers))
        await unsubscribe.finish("取消订阅成功！")
    except nonebot.exception.FinishedException:
        pass
    except:
        await unsubscribe.finish("你还没有订阅过日报推送！")

test = on_command("test")


@test.handle()
@utils.permission_required(99)
async def handle_event(event: V11Event):
    await test.finish("测试成功！")
