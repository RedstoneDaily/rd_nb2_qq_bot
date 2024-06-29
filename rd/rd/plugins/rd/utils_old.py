import json
import nonebot_plugin_localstore as store

def get_args(event):
    # 从消息中提取参数
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


def get_permission(qq, ops_list = json.loads(store.get_data_file("rd", "ops.json").read_text())):
    """
    获取用户权限
    """
    try:
        for op in ops_list:  # 遍历ops列表
            if op["qq_number"] == int(qq):
                return op["permission"]  # 返回权限
    except:
        return 0  # 没有权限

    return 0  # 没有权限