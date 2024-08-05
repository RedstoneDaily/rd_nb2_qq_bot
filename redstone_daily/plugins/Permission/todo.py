from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event

from redstone_daily.plugins.utils import permission_required, get_database, get_context

todo_del_matcher = on_command(
    'todo del', force_whitespace=True, priority=10, block=True)

todo_del_all_matcher = on_command(
    'todo del_all', force_whitespace=True, priority=10, block=True)

db = get_database('todo').get_db()


@todo_del_matcher.handle()
@permission_required(9)
async def handle_todo_del(event: Event):
    sender, arg, group = get_context(event)

    if len(arg) <= 1:
        await todo_del_matcher.finish('请输入待办事项id')

    db.delete_one({'type': 'todo', 'id': int(arg[1])})

    await todo_del_matcher.finish('已删除待办事项')


@todo_del_all_matcher.handle()
@permission_required(10)
async def handle_todo_del_all(event: Event):
    sender, arg, group = get_context(event)

    if len(arg) > 1 and arg[1] == 'confirm':
        db.delete_many({'type': 'todo'})
        db.find_one_and_update(
            {'type': 'config'},
            {'$set': {'max_id': 0}},
            projection={'max_id': True, '_id': False},
            upsert=True
        )

        await todo_del_all_matcher.finish('已删除所有待办事项')

    else:
        await todo_del_all_matcher.finish('请输入 "todo del_all confirm" 以确认删除所有待办事项')