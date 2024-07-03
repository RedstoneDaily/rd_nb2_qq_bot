import time
import json, random

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.rule import to_me
from nonebot.plugin import *
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot import require

from redstone_daily.plugins.utils import get_context, User

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

"""
娱乐功能
"""

divine = on_command("luck", aliases={'运势', '人品', '今日人品', 'jrrp'})


@divine.handle()
async def handle_divine(event: Event):
    """
    今日人品
    """

    _time = time.time()  # 获取当前时间
    sender = event.user_id  # 取出发送者
    random.seed(int(sender) + int(_time - _time % 86400))  # 设置随机种子

    await divine.finish(f"你今天的运势是：{random.randint(1, 200)}%"
                        if random.randint(1, 1000) != 1 else "你今天的运势是：114514%")  # 发送随机数


'''at_bot = on_message(rule=to_me())

@at_bot.handle()
async def at():
    """
    处理@机器人
    :return:
    """

    await at_bot.finish("喵喵喵? 喵喵喵, /rdhelp 喵喵喵喵喵!")'''

welcome = on_command("welcomenew")


@welcome.handle()
async def welcome_new():
    """
    新用户欢迎
    """
    await welcome.finish("欢迎新朋友！\n"
                         "使用 /rdhelp 获取更多信息")


dice = on_command("dice", aliases={'命运骰子', '命运色子'})


@dice.handle()
async def handle_dice(event: GroupMessageEvent):
    """
    骰子
    指定一位成员参与, 随机禁言成员或者发送者
    """
    sender, arg, group = get_context(event)

    if len(arg) > 0:  # 指定了参与者
        num = random.randint(1, 20000) / 1000
        await dice.send(f"你向{arg[0]}投出了一枚命运的骰子...")
        time.sleep(1)

        if num <= 5:  # 骰子点数小于等于5, 禁言玩家
            await group.mute(User(int(arg[0])), int(((6 - num) * 5) ** 2))
            await dice.finish(f"骰子停下了...{arg[0]}被禁言了{int(((6 - num) * 5) ** 2)}秒")
        else:  # 骰子点数大于5, 禁言发送者
            await group.mute(sender, int(((num - 1) * 5) ** 2))
            await dice.finish(f"骰子停下了...玩弄命运者终将受到惩罚, 你被禁言了{int(((num - 1) * 5) ** 2)}秒")