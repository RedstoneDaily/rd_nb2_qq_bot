"""
import datetime, time
import json, random

from nonebot.rule import to_me
from nonebot.plugin import *
import requests, nonebot
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot.adapters.onebot.v11 import Event as V11Event
from nonebot import require, get_bot

from nonebot_plugin_apscheduler import scheduler

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store
"""
from nonebot import require
require("nonebot_plugin_apscheduler")

from .games import *

"""
所有的娱乐功能
"""

from .daily import *

"""
日报的获取与推送
"""

from .help import *

"""
帮助信息
"""

from .op import *

"""
操作指令
"""

from .manage import *

"""
群管指令
"""

from rd.rd.plugins.rd.utils.database import *
# scheduler.add_job(run_every_day, "cron", hour=16, minute=30, next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=1))  # 每天16:30执行一次
