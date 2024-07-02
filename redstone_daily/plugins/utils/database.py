import pymongo
import nonebot
from copy import deepcopy
from nonebot.plugin import *
# 获取配置文件
_config = nonebot.get_driver().config

# 读取配置文件
host = _config.db_host
port = _config.db_port
username = _config.db_username
password = _config.db_password

# 连接数据库
client = pymongo.MongoClient(host, port, username=username, password=password)


class Database:
    def __init__(self):
        # 初始化数据库
        self.database = client['qq_bot']
        self.collection = None

    def set_collection(self, collection_name):
        # 设置使用的集合
        self.collection = self.database[collection_name]

    def get(self, query_dict):
        # 查询数据
        query_result = self.collection.find_one(query_dict)
        del query_result['_id']
        return query_result

    def get_db(self):
        # 获取集合实例
        return self.collection

    def clear(self):
        # 清空集合
        self.collection.delete_many({})

# 导出数据库
def get_database(collection_name):
    # 获取数据库实例
    db = Database()
    db.set_collection(collection_name)
    return db