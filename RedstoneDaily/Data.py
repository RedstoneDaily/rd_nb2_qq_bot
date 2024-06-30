from pathlib import Path
from json import load, dump

from nonebot import require
from nonebot.log import logger

require('nonebot_plugin_localstore')
from nonebot_plugin_localstore import get_data_file


class Data:
    # 数据文件的路径和数据内容
    file_path: Path = None
    data: (dict | list) = {}

    def __init__(self, file_name, defualt: (dict | list) = {}):
        self.data = defualt
        self.file_path = file_name

    def load(self):
        # 加载数据文件
        self.file_path = get_data_file('RedstoneDaily', self.file_path)
        if self.file_path.exists():
            with self.file_path.open('r', encoding='Utf-8') as file:
                self.opreation_permissions = load(file)
            logger.success(F'Data in "{self.file_path}" loaded successfully.')
            return None
        logger.warning('Data was not found, creating a new one now.')
        self.save()

    def save(self):
        # 保存数据到文件
        with self.file_path.open('w', encoding='Utf-8') as file:
            dump(self.data, file, indent=4)
        logger.success(F'Data saved successfully.')


# 订阅者数据对象
Subscribers = Data('subscribers.json', [])
# 操作权限数据对象
OpreationPermissions = Data('opreation_permissions.json', {'2101596336': 10})

# 数据对象列表
DataObjects = (OpreationPermissions, Subscribers)