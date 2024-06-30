import json

from .decorators import *
from .user import *
from .group import *
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11 import Event

def get_context(event: Event):
    """
    获取事件的上下文信息(发送者的utils.user.User对象, 指令参数, 群聊的utils.group.Group对象(如果是群聊消息))
    :param event: 事件对象
    :return: 事件的上下文信息(格式为[user, args, group])
    """

    def get_args(event: Event):
        """
        获取指令参数
        :param event: 事件对象
        :return: 指令参数列表
        """
        args = []
        json_data = json.loads(event.json())
        for msg in json_data['original_message']:  # 遍历消息列表
            if msg['type'] == 'text':  # 找到文本消息
                for i in msg['data']['text'].split(' '):  # 遍历文本

                    if i.startswith('/'):  # 忽略命令
                        continue

                    args.append(i)
            if msg['type'] == 'at':  # 找到@消息
                args.append(msg['data']['qq'])

        for i in args:  # 去除空白字符
            if i == '':
                args.remove(i)

        return args

    if isinstance(event, GroupMessageEvent):
        group = Group(event.group_id)
    else:
        group = None

    user = User(event.user_id)
    args = get_args(event)

    return [user, args, group]
