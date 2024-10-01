import time
import json, random

from nonebot.rule import to_me
from nonebot.plugin import *
from nonebot.adapters import Message
from nonebot.params import CommandArg, Event
from nonebot import require

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

"""
娱乐功能
"""

divine = on_command("今日人品")


@divine.handle()
async def handle_divine(event: Event):
    """
    今日人品
    :return:
    """

    _time = time.time()  # 获取当前时间
    sender = event.user_id  # 取出发送者
    random.seed(int(sender) + int(_time - _time % 86400))  # 设置随机种子

    await divine.finish(f"你今天的运势是：{random.randint(1, 100)}")  # 发送随机数


'''at_bot = on_message(rule=to_me())

@at_bot.handle()
async def at():
    """
    处理@机器人
    :return:
    """

    await at_bot.finish("喵喵喵? 喵喵喵, /help 喵喵喵喵喵!")'''

welcome = on_command("welcomenew")


@welcome.handle()
async def welcome_new():
    """
    新用户欢迎
    """
    await welcome.finish("欢迎新朋友！\n"
                         "使用 /help 获取更多信息")


point24 = on_command("24point")


@point24.handle()
async def twenty_four_point(event: Event, args: Message = CommandArg()):
    """
    24点游戏
    """

    async def generate_points():
        """
        生成4位数字
        """
        points = []
        for i in range(4):
            points.append(str(random.randint(1, 13)))  # 随机生成4位数字

        point24_dict.append({"qq_number": sender, "points": points})  # 添加数据
        point24_data_file.write_text(json.dumps(point24_dict))  # 存储数据

        await point24.finish(f"24点游戏:\n"
                             f"  {points[0]} {points[1]} {points[2]} {points[3]}\n"
                             "使用 /24point answer {你的答案} 猜测答案, 需要英文括号, 乘法与除法使用 * 和 / 符号\n"
                             "使用 /24point giveup 放弃游戏")

    sender = event.user_id  # 取出发送者
    arg = str(args.extract_plain_text()).split(' ')  # 取出参数

    point24_data_file = store.get_data_file("rd", "24point.json")  # 读取24点游戏数据

    try:
        point24_data = point24_data_file.read_text()  # 读取数据
    except:
        point24_data = '[]'
        point24_data_file.write_text(point24_data)

    point24_dict = json.loads(point24_data)  # 解析数据
    for i in point24_dict:
        if i["qq_number"] == int(sender):
            if arg[0] == "giveup":  # 放弃游戏
                point24_dict.remove(i)  # 删除数据
                point24_data_file.write_text(json.dumps(point24_dict))  # 存储数据
                await point24.finish("你放弃了游戏！")

            elif arg[0] == "answer":  # 回答游戏
                # 处理参数
                arg.pop(0)  # 去掉指令
                answer = ''
                for j in arg:
                    answer += j + ' '

                try:
                    for j in answer:  # 检查注入攻击
                        if j not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '-', '*', '/', ' ', '(',
                                     ')']:
                            await point24.finish("检测到注入攻击！")

                    # 检查是否有其他数字参与运算
                    for j in i["points"]:
                        answer_old = answer  # 备份答案
                        answer = answer.replace(str(j), '', 1)  # 替换数字
                        if answer == answer_old:
                            await point24.finish("数字需要全部参与运算！")

                    if any(char.isdigit() for char in answer):  # 还有数字参与运算
                        await point24.finish("有题干之外的数字参与运算！")

                    answer = answer_old  # 恢复答案

                    if eval(answer) == 24:  # 回答正确
                        point24_dict.remove(i)  # 删除数据
                        point24_data_file.write_text(json.dumps(point24_dict))  # 存储数据-
                        await point24.send("恭喜你答对了！")
                        await generate_points()  # 开始下一轮游戏

                except ZeroDivisionError:  # 除数为0
                    await point24.finish("不能除以0！")

                else:  # 回答错误
                    await point24.finish("很遗憾，您答错了！")

            else:  # 开始过游戏
                await point24.finish("你已经开始过游戏了！\n"
                                     f"  {i["points"][0]} {i["points"][1]} {i["points"][2]} {i["points"][3]}\n"
                                     "使用 /24point answer {你的答案} 猜测答案, 使用英文括号, 乘法与除法使用 * 和 / 符号\n"
                                     "使用 /24point giveup 放弃游戏")
    await generate_points()  # 开始游戏


minesweeper = on_command("minesweeper")


@minesweeper.handle()
async def minesweeper_game(event: Event, args: Message = CommandArg()):
    """
    扫雷游戏
    """
    arg = str(args.extract_plain_text()).split(' ')  # 取出参数

    def generate_board(width, height, mines):
        """
        生成游戏板
        """
        board = []
        for i in range(width):  # 行
            row = []
            for j in range(height):  # 列
                row.append(0)
            board.append(row)

        def generate_mine(mines, board):

            if mines == 0:  # 所有雷已生成
                return board

            x = random.randint(0, width - 1)  # 随机生成雷的位置
            y = random.randint(0, height - 1)

            if board[x][y] == -1:
                return generate_mine(mines, board)  # 重复生成

            board[x][y] = -1
            mines -= 1
            return generate_mine(mines, board)  # 递归生成雷

        board = generate_mine(mines, board)  # 生成雷

        for x in range(width):  # 计算数字
            for y in range(height):
                if board[x][y] == -1:  # 雷
                    continue

                else:
                    count = 0  # 计算周围雷数

                    for x_offset in [-1, 0, 1]:  # 计算周围雷数
                        for y_offset in [-1, 0, 1]:
                            if x_offset == 0 and y_offset == 0:  # 跳过中心
                                continue

                            if 0 <= x + x_offset < width and 0 <= y + y_offset < height:  # 周围在游戏板内
                                if board[x + x_offset][y + y_offset] == -1:
                                    count += 1

                    board[x][y] = count  # 填充数字

        return board

    def show_board(board, mask):
        """
        显示游戏板
        """
        x_hint = ['⒈', '⒉', '⒊', '⒋', '⒌', '⒍', '⒎', '⒏', '⒐', '⒑', '⒒', '⒓', '⒔', '⒕']  # 横坐标提示
        y_hint = ['⑴', '⑵', '⑶', '⑷', '⑸', '⑹', '⑺', '⑻', '⑼', '⑽', '⑾', '⑿', '⒀', '⒁']  # 纵坐标提示
        nums = ['□', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']  # 数字

        string = '□' + x_hint[0:width]

        for i in range(height):
            string += '\n' + y_hint[i]

            for j in range(width):
                if mask[j][i] == 1:  # 已打开
                    string += nums[board[j][i]]

                else:  # 未打开
                    string += '■'

        minesweeper.finish(string)

    sender = event.user_id  # 取出发送者

    minesweeper_data_file = store.get_data_file("rd", "minesweeper.json")  # 读取扫雷游戏数据

    try:
        minesweeper_data = minesweeper_data_file.read_text()
    except:  # 第一次玩游戏
        minesweeper_data = []
        minesweeper_data_file.write_text(json.dumps(minesweeper_data))  # 存储数据

    minesweeper_data = json.loads(minesweeper_data_file.read_text())  # 解析数据

    for i in minesweeper_data:
        if i["qq_number"] == int(sender):  # 玩过游戏
            pass

    else:  # 第一次玩游戏
        if len(arg) == 0:  # 无参数
            width = 9
            height = 9
            mines = 15
        elif len(arg) == 1:  # 单参数
            if arg[0] == 'easy':  # 简单模式
                width = 7
                height = 7
                mines = 7
            elif arg[0] == 'normal':  # 普通模式
                width = 9
                height = 9
                mines = 15
            elif arg[0] == 'hard':  # 困难模式
                width = 14
                height = 14
                mines = 35
            else:  # 无效参数
                await minesweeper.finish("无效参数！\n"
                                         "使用 /minesweeper easy/normal/hard 开始游戏")
        else:  # 无效参数
            await minesweeper.finish("无效参数！\n"
                                     "使用 /minesweeper easy/normal/hard 开始游戏")

        board = generate_board(width, height, mines)  # 生成游戏板
        mask = [[1] * height for _ in range(width)]  # 掩模

        minesweeper_data.append({"qq_number": sender, "board": board, "mask": mask})  # 添加数据
        minesweeper_data_file.write_text(json.dumps(minesweeper_data))  # 存储数据

        show_board(board, mask)
