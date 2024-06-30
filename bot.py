import nonebot
from nonebot.adapters.onebot.v11 import Adapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 在这里加载插件
nonebot.load_builtin_plugins('echo')  # 内置插件
nonebot.load_plugins('redstone_daily/plugins')  # 本地插件


@driver.on_startup
def startup():
    # 在启动时加载数据对象
    from redstone_daily import Data
    for data in Data.DataObjects:
        data.load()


@driver.on_shutdown
def shutdown():
    from redstone_daily import Data
    # 在关闭时保存数据对象
    for data in Data.DataObjects:
        data.save()


# 运行 NoneBot
if __name__ == '__main__':
    nonebot.run()
