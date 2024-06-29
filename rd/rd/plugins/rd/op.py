import json

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.plugin import *
import nonebot
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot import require
from .utils_old import get_args, get_permission

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store


op = on_command("op")

"""
OP指令
"""

reset_ops = on_command("reset_ops")

@reset_ops.handle()
async def reset_ops_cmd(event: Event):
    """
    重置ops列表
    """
    sender = event.user_id  # 取出发送者

    # if int(sender) == 3327018890:  # 只有创建者可以执行此操作
    ops = store.get_data_file("rd", "ops.json")  # 读取ops列表
    ops.write_text('[{"qq_number": 3327018890, "permission": 100}]')  # 清空ops数据
    await reset_ops.finish("ops数据已重置！")
    #else:
    await reset_ops.finish("你没有权限执行此操作！")

@op.handle()
async def op_cmd(event: GroupMessageEvent):
    """
    OP指令
    """
    arg = get_args(event)  # 取出参数
    sender = event.user_id  # 取出发送者

    ops = store.get_data_file("rd", "ops.json")  # 读取ops列表
    try:
        ops_data = ops.read_text()  # 读取ops数据
        ops_list = json.loads(ops_data)  # 解析ops数据

        if get_permission(sender, ops_list) > 0:
            # 处理参数
            if len(arg) > 0:
                if arg[0] == "clear_sub":
                    if get_permission(sender, ops_list) <= 95:  # 权限不够
                        await op.finish(
                            f"你需要95级以上权限才能执行此操作！你的权限为: {get_permission(sender, ops_list)}")

                    # 清空订阅
                    subscribers = store.get_data_file("rd", "subscribe.json")
                    subscribers.write_text('[]')
                    await op.finish("订阅已清空！")

                elif arg[0] == "add":
                    # 添加OP
                    for i in ops_list:
                        if int(arg[1]) == i["qq_number"]:  # 已经是OP
                            await op.finish(f"{int(arg[1])}已经是OP了！")

                    if get_permission(sender, ops_list) <= int(arg[2]):  # 权限不够
                        await op.finish("添加的用户权限不能高于你的权限！")

                    ops_list.append({"qq_number": int(arg[1]), "permission": int(arg[2])})  # 添加OP
                    ops.write_text(json.dumps(ops_list))
                    await op.finish(f"添加成功！{int(arg[1])}已成为OP, 现存OP：{ops_list}")

                elif arg[0] == "rm":
                    # 删除OP
                    if get_permission(sender, ops_list) <= get_permission(int(arg[1]), ops_list):  # 权限不够
                        await op.finish("不能删除高权限用户！")

                    if get_permission(sender, ops_list) < 0:
                        await op.finish(f"{arg[1]}不是OP！")  # 不是OP

                    ops_list.remove(
                        {"qq_number": int(arg[1]), "permission": get_permission(int(arg[1]), ops_list)})  # 删除OP
                    ops.write_text(json.dumps(ops_list))
                    await op.finish(f"删除成功！{arg[1]}已不再是OP, 现存OP：{ops_list}")

                elif arg[0] == "get_perm":
                    # 获取权限

                    try:  # 带参数
                        await op.finish(f"{arg[1]}的权限为{get_permission(int(arg[1]), ops_list)}")
                    except:  # 无参数
                        # 获取自己权限
                        await op.finish(f"你的权限为{get_permission(sender, ops_list)}")

                elif arg[0] == "query_sub":
                    # 查询订阅
                    subscribers = store.get_data_file("rd", "subscribe.json")  # 读取订阅列表
                    subscribers_data = subscribers.read_text()
                    subscribers_list = json.loads(subscribers_data)

                    if int(arg[1]) in subscribers_list:  # 订阅了
                        await op.finish(f"{arg[1]}订阅了日报推送！")
                    else:  # 没有订阅
                        await op.finish(f"{arg[1]}没有订阅日报推送！")

                elif arg[0] == "rm_sub":
                    # 删除订阅
                    if get_permission(sender, ops_list) <= 25:  # 权限不够
                        await op.finish(
                            f"你需要25级以上权限才能执行此操作！你的权限为: {get_permission(sender, ops_list)}")

                    subscribers = store.get_data_file("rd", "subscribe.json")  # 读取订阅列表
                    subscribers_data = subscribers.read_text()
                    subscribers_list = json.loads(subscribers_data)

                    if int(arg[1]) in subscribers_list:  # 订阅了
                        subscribers_list.remove(int(arg[1]))  # 删除订阅
                        subscribers.write_text(json.dumps(subscribers_list))
                        await op.finish(f"{arg[1]}取消订阅成功！")
                    else:  # 没有订阅
                        await op.finish(f"{arg[1]}没有订阅日报推送！")

                elif arg[0] == "add_sub":
                    # 添加订阅
                    if get_permission(sender, ops_list) <= 45:  # 权限不够
                        await op.finish(
                            f"你需要45级以上权限才能执行此操作！你的权限为: {get_permission(sender, ops_list)}")

                    subscribers = store.get_data_file("rd", "subscribe.json")  # 读取订阅列表
                    subscribers_data = subscribers.read_text()
                    subscribers_list = json.loads(subscribers_data)

                    if int(arg[1]) not in subscribers_list:  # 没有订阅
                        subscribers_list.append(int(arg[1]))  # 添加订阅
                        subscribers.write_text(json.dumps(subscribers_list))
                        await op.finish(f"{arg[1]}订阅成功！")
                    else:  # 已经订阅
                        await op.finish(f"{arg[1]}已经订阅过日报推送！")
                elif arg[0] == "clear_24point":
                    # 清空24点游戏数据
                    point24_data_file = store.get_data_file("rd", "24point.json")  # 读取24点游戏数据
                    point24_data_file.write_text('[]')  # 清空数据
                    await op.finish("24点游戏数据已清空！")
                elif arg[0] == "get_file":
                    # 获取文件
                    try:
                        file_path = arg[1]
                        file = store.get_data_file("rd", file_path)
                        await op.finish(file.read_text())
                    except nonebot.exception.FinishedException:
                        pass
                    except Exception as e:
                        await op.finish(f"获取文件失败！{e}")
                elif arg[0] == "set_file":
                    # 设置文件
                    if get_permission(sender, ops_list) < 99:  # 权限不够
                        await op.finish(
                            f"你需要99级以上权限才能执行此操作！你的权限为: {get_permission(sender, ops_list)}")
                    try:
                        file_path = arg[1]
                        arg.pop(0)  # 去掉指令
                        arg.pop(0)  # 去掉文件路径
                        file_content = ''
                        for i in arg:
                            file_content += i + ' '  # 合并参数
                        file_content = json.loads(file_content)  # 解析参数
                        file = store.get_data_file("rd", file_path)
                        file.write_text(json.dumps(file_content))
                        await op.finish(f"文件{file_path}已设置！")
                    except nonebot.exception.FinishedException:
                        pass
                    except Exception as e:
                        await op.finish(f"设置文件失败！{e}")
                else:
                    await op.finish("未知指令！")

        else:
            await op.finish("你没有权限执行此操作！")
    except nonebot.exception.FinishedException:
        pass
    except Exception as e:
        raise e
        await op.finish(str(e))