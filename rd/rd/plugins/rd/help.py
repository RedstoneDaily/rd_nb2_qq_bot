from nonebot.plugin import *
from nonebot.adapters import Message
from nonebot.params import CommandArg

"""
所有帮助信息都在这里qwq
"""

_help = on_command("help")

@_help.handle()
async def rd_help():
    """
    显示帮助信息
    """
    await _help.finish("RD QQ Bot帮助\n---------\n"
                      "指令大全: /commands\n"
                      "使用教程: /tutorial\n"
                      "关于rd: /about\n"
                      "---------")


commands = on_command("commands")


@commands.handle()
async def rd_commands(args: Message = CommandArg()):
    """
    显示指令列表
    """
    arg = args.extract_plain_text().split(' ')  # 取出参数

    commands_list = [
        "最新日报: /latest",
        "帮助信息: /help",
        "指令列表: /commands",
        "使用教程: /tutorial",
        "关于我们: /about",
        "订阅日报推送: /sub",
        "取消日报推送: /unsub",
        "新用户欢迎: /welcomenew",
        "OP指令: /op",
        "24点游戏: /24point",
        "禁言: /mute",
        "修改昵称: /set_nickname",
        "修改头衔: /set_title",
        "踢出群聊: /kick",
        "封禁: /ban",
    ]

    async def send_commands(start, end, page):
        commands_str = ""
        for i in range(start, end):
            commands_str += commands_list[i] + "\n"  # 构造字符串

        await commands.finish(f"RD QQ Bot指令列表 第{page} / {int(len(commands_list) / 10) + 1}页\n---------\n"
                              f"{commands_str}"
                              f"---------")

    if len(arg) >= 1:  # 处理参数
        page = int(arg[0]) if arg[0].isdigit() else 1  # 处理页码

        if page <= 0:
            await commands.finish("页码必须为正整数")

        start = (page-1)*10  # 计算开始位置
        end = page*10  # 计算结束位置
        if end > len(commands_list):   # 处理页码超出范围
            end = len(commands_list) - 1

        if start > len(commands_list):  # 处理页码超出范围
            await commands.finish("页码超出范围")

        await send_commands(start, end, page)


tutorial = on_command("tutorial")


@tutorial.handle()
async def rd_tutorial(args: Message = CommandArg()):
    """
    显示使用教程
    """
    command = args.extract_plain_text()  # 取出指令

    # 处理参数
    if command:
        if command == "latest":
            await tutorial.finish("/latest 显示最新一期的日报\n"
                                  "参数: 无需参数")
        elif command == "rdhelp":
            await tutorial.finish("/help 显示帮助信息\n"
                                  "参数: 无需参数")
        elif command == "commands":
            await tutorial.finish("/commands 显示指令列表\n"
                                  "参数: 无需参数")
        elif command == "about":
            await tutorial.finish("/about 关于我们的信息\n"
                                  "参数: 无需参数")
        elif command == "tutorial":
            await tutorial.finish("/tutorial 显示使用教程\n"
                                  "参数: [command] 查看此指令的详细教程")
        elif command == "sub":
            await tutorial.finish("/sub 订阅日报推送\n"
                                  "参数: 无需参数")
        elif command == "unsub":
            await tutorial.finish("/unsub 取消日报推送\n"
                                  "参数: 无需参数")
        elif command == "welcome":
            await tutorial.finish("/welcomenew 新用户欢迎\n"
                                  "参数: 无需参数")
        elif command == "op":
            await tutorial.finish("/op OP指令\n"
                                  "参数: {command} [args]\n"
                                  "OP指令列表:\n"
                                  "/op clear_sub  清空订阅\n"
                                  "/op add {qq_number} {permission}  添加OP\n"
                                  "/op rm {qq_number}  删除OP\n"
                                  "/op get_perm [qq_number]  获取自己的权限\n"
                                  "/op query_sub {qq_number}  查询订阅\n"
                                  "/op rm_sub {qq_number}  删除订阅\n"
                                  "/op add_sub {qq_number}  添加订阅\n"
                                  "/op clear_24point  清空24点游戏数据\n"
                                  "/op get_file {file_path}  获取文件\n"
                                  "/op set_file {file_path} {file_content}  设置文件")
        elif command == "24point":
            await tutorial.finish("/24point 24点游戏\n"
                                  "参数: [option]"
                                  "option: 无: 开始游戏 answer {your_answer}: 回答游戏 giveup: 放弃游戏\n")
        elif command == "mute":
            await tutorial.finish("/mute 禁言\n"
                                  "参数: {qq_number} {duration} 禁言指定用户\n"
                                  "duration用法: \n"
                                  "示例: 30s: 30秒 根据后缀字母 s/m/h/d 表示秒/分/时/天")
        elif command == "set_nickname":
            await tutorial.finish("/set_nickname 修改昵称\n"
                                  "参数: {qq_number} {new_nickname}")
        elif command == "set_title":
            await tutorial.finish("/set_title 修改头衔\n"
                                  "参数: {qq_number} {new_title}")
        elif command == "kick":
            await tutorial.finish("/kick 踢人\n"
                                  "参数: {qq_number} 踢出指定用户")
        elif command == "ban":
            await tutorial.finish("/ban 封禁\n"
                                  "参数: {qq_number}封禁指定用户")
        else:
            await tutorial.finish("指令不存在")
    else:
        await tutorial.finish("RD QQ Bot使用教程\n---------\n"
                              "常规指令格式: /指令 选项1 选项2\n"
                              "使用/tutorial 指令名 查看该指令的详细教程\n"
                              "选填参数[会以这种格式显示], 必填参数{会以这种格式显示}\n"
                              "---------")


about = on_command("about")


@about.handle()
async def rd_about():
    """
    显示关于我们信息
    """
    await about.finish("红石日报Redstone Daily是一个开源非盈利的网站项目，收集跟进全网红石科技最新前沿进展，并以日报、周报、月报以及年报的形式发布。\n"
                       "更多信息请访问：https://www.rsdaily.com/ https://redstone-daily.notion.site/Redstone-Daily-7e55265d870b424594c74acb65e3f62a\n"
                       "RD QQ Bot作者: @creepebucket(creepebucket@qq.com), @LonelySail(xiaocaicai_email@sina.com),@So_Cute_Hamster(1754005120@qq.com)")
