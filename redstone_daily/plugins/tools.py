import json
from datetime import datetime

import requests
from nonebot.plugin.on import on_command

from redstone_daily.plugins.utils import get_context

bili_matcher = on_command('bili', aliases={'查成分', '查用户'})

@bili_matcher.handle()
async def bili(event):
    sender, arg, group = get_context(event)

    if not (arg and arg[0].isdigit()):
        await bili_matcher.finish('请输入正确的用户 UID')

    if len(arg) > 1 and arg[1].isdigit():
        if int(arg[1]) > 100:
            await bili_matcher.finish('查询数量不能超过 100')
        else:
            count = int(arg[1])
    else:
        count = 10

    # 构造API请求地址
    url = f'https://api.aicu.cc/api/v3/search/getreply?uid={arg[0]}&pn=1&ps=100&mode=0'

    # 发起API请求
    response = requests.get(url)

    # 解析API响应数据
    data = response.json()

    # 格式化输出
    if data['code'] != 0:
        await bili_matcher.finish('查询失败，返回信息：\n' + json.dumps(data, indent=4))

    reply = f'用户 UID {arg[0]} 最近评论如下：'

    for i in data['data']['replies'][:count]:
        reply += f'\n{datetime.fromtimestamp(i["time"]).strftime("%Y-%m-%d %H:%M:%S")}：{i["message"]}'

    await bili_matcher.finish(reply)