import nonebot
import requests
from datetime import datetime
import cloudflare, pytz
from cloudflare.types.pages import (
    Deployment,
    Project,
    Stage,
)

from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from redstone_daily.plugins.Config import config
from redstone_daily.plugins.utils import get_database, permission_required, get_context, User

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
async def handle_page(event: GroupMessageEvent):
    
    sender, arg, group = get_context(event)
    
    if len(arg) == 0 or len(arg) == 1 and arg[0] == 'info':
        await handle_page_info(event)
    elif len(arg) == 2 and arg[0] == 'del':
        await handle_page_del(event)


async def handle_page_info(event: Event):

    await page_matcher.send('正在查询最新测试页面...')
    message = ''
    
    try:
        # https://github.com/cloudflare/cloudflare-python
        # https://developers.cloudflare.com/api/operations/pages-deployment-get-deployments
        client = cloudflare.AsyncCloudflare(api_token=config.cf_api_token)
        results = {}
        project = await client.pages.projects.get(
            account_id=config.cf_account_id,
            project_name=config.cf_project_name
        )

        async for deployment in await client.pages.projects.deployments.list(
            account_id=config.cf_account_id,
            project_name=config.cf_project_name
        ):
            url = f'https://{project.subdomain}' if deployment.environment == 'production' else (deployment.aliases or [None])[0]
            if not url is None and results.get(url) is None:
                results[url] = deployment
        
        if results.keys():
            sorted_urls = sorted(results.keys(), key=lambda x: x[::-1])     # sort by reverse
            message = "戳我查看:\n" + "\n".join(f"→{url}←" for url in sorted_urls)
        else:
            message = "没有找到任何部署喵~"
        
    except cloudflare.APIConnectionError as e:
        message = f"查询失败，API连接错误\n原因：{e.__cause__}"
    except cloudflare.RateLimitError as e:
        message = "查询失败，API请求频率已达上限"
    except cloudflare.APIStatusError as e:
        message = f"查询失败，状态码：{e.status_code}\n错误信息：\n{e.response}"
    
    await page_matcher.finish(message)


@permission_required(9)
async def handle_page_del(event: GroupMessageEvent):

    sender, arg, group = get_context(event)
    target_branch = arg[1]

    await page_matcher.send(f"正在删除与分支\"{target_branch}\"关联的部署...")
    message = ''

    try:
        # https://github.com/cloudflare/cloudflare-python
        # https://developers.cloudflare.com/api/operations/pages-deployment-get-deployments
        client = cloudflare.AsyncCloudflare(api_token=config.cf_api_token)

        selected_deployments: list[Deployment] = []
        async for deployment in await client.pages.projects.deployments.list(
            account_id=config.cf_account_id,
            project_name=config.cf_project_name
        ):
            if deployment.id is None:
                continue
            metadata = deployment.deployment_trigger.metadata if deployment.deployment_trigger is not None else None
            branch = metadata.branch if metadata is not None else None
            if branch == target_branch:
                selected_deployments.append(deployment)
                await client.pages.projects.deployments.delete(
                    account_id=config.cf_account_id,
                    project_name=config.cf_project_name,
                    deployment_id=deployment.id
                )

        message = f"已删除与分支\"{target_branch}\"关联的{len(selected_deployments)}个部署。"

    except cloudflare.APIConnectionError as e:
        message = f"操作失败，API连接错误\n原因：{e.__cause__}"
    except cloudflare.RateLimitError as e:
        message = "操作失败，API请求频率已达上限"
    except cloudflare.APIStatusError as e:
        message = f"操作失败，状态码：{e.status_code}\n信息：\n{e.response}"
    
    await page_matcher.finish(message)