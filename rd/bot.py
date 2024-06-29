import nonebot
from nonebot.adapters.onebot import V11Adapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)


# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugin("nonebot_plugin_addFriend")
nonebot.load_plugins("rd/plugins")  # 本地插件


# 运行 NoneBot
if __name__ == "__main__":
    nonebot.run()