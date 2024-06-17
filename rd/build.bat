python -m pip install --user pipx
python -m pipx ensurepath
pipx install nb-cli
pip install 'nonebot2[fastapi]'
pip install nonebot-adapter-console
nb plugin install nonebot_plugin_addFriend
nb plugin install nonebot_plugin_apscheduler
nb plugin install nonebot_plugin_localstore
nb run