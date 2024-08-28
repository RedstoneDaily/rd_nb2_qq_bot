import nonebot
import requests
from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin.on import on_command

from redstone_daily.plugins.Config import config
from redstone_daily.plugins.utils import get_database

"""
查询服务器状态
"""


def run_test_points(test_points: list):
    """
    测试点
    :param test_points: 测试点列表
    :return: 测试结果
    """
    result = {'all_points': 0, 'passed': 0, 'failed': 0, 'failed_details': []}  # 测试结果

    for point in test_points['points']:  # 遍历测试点
        result['all_points'] += 1
        try:
            response = requests.get(point['url'])  # 发送请求
            if response.status_code == 200:  # 请求成功
                result['passed'] += 1
            else:  # 请求失败
                result['failed'] += 1
                result['failed_details'].append(f"{point['name']} - {response.status_code}")
        except Exception as e:  # 请求异常
            result['failed'] += 1
            result['failed_details'].append(f"{point['name']} - {e}")

    return result


def get_test_points():
    """
    获取测试点
    :return: 测试点列表
    """
    # 从数据库获取测试点
    db = get_database('test_points').collection

    return db.find()


status_matcher = on_command('status')


@status_matcher.handle()
async def handle_status(event: Event):
    test_points = get_test_points()

    await status_matcher.send('正在查询服务器状态...')

    all_points = 0  # 总测试点数
    passed_points = 0  # 通过测试点数
    failed_points = 0  # 失败测试点数

    for points in test_points:  # 遍历测试点
        result = run_test_points(points)  # 执行测试

        all_points += result['all_points']  # 记录数据
        passed_points += result['passed']
        failed_points += result['failed']

        # 发送测试结果
        message = f"测试点 - {points['name']} 状态：\n"  # 消息内容
        message += f"共{result['all_points']}个测试点，通过{result['passed']}个，失败{result['failed']}个。"
        if result['failed'] > 0:
            message += "\n失败详情："
            for detail in result['failed_details']:
                message += f"\n{detail}"

        await status_matcher.send(message)

    await status_matcher.send(f"所有测试点均已完成，总共{all_points}个测试点，通过{passed_points}个，失败{failed_points}个，"
                              f"通过率{passed_points/all_points*100:.2f}%。")


page_matcher = on_command('dev', aliases={'page'})

@page_matcher.handle()
async def handle_page(event: Event):
    await page_matcher.send('正在查询最新测试页面...')

    url = (f'https://api.cloudflare.com/client/v4/accounts/{config.cf_account_id}'
           f'/pages/projects/{config.cf_project_name}/deployments')
    headers = {'Authorization': f'Bearer {config.cf_api_token}',}

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        await page_matcher.finish(f"戳我查看:\n→{data['result'][0]['url']}←")

    else:
        await page_matcher.finish(f"查询失败，错误：{data}, url={url}")