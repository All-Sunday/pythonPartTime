# @Description: peewee连接数据库 控制只允许一个程序在运行
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/18 14:37
# @File : seleninm.py

from peewee import *
import time

db = MySQLDatabase("yidong", host="124.221.131.73", port=3306, user="yidong", passwd="wxp8GtjHPNDLzYNE")



class BaseModel(Model):
    class Meta:
        database = db


class Run(BaseModel):
    times = IntegerField()
    update_time = IntegerField()

    class Meta:
        table_name = 'run'


# now_timestmap = int(time.time())
# print(now_timestmap)
# book = Run(times=now_timestmap, update_time=now_timestmap)
# book.save()
# r = Run.create(times=now_timestmap, update_time=now_timestmap)
# print(r.times)

# Run.insert(times=now_timestmap, update_time=now_timestmap).execute()
# for book in Run.filter():
#     print(book.times)

# 启动程序
def sql_start():
    # 删除所有更新时间超过五分钟的记录
    now_timestmap = int(time.time())
    print(now_timestmap - 300)
    # runs = Run.select().where(Run.update_time < now_timestmap - 300)
    Run.delete().where(Run.update_time < now_timestmap - 300).execute()

    # 查询剩余记录数 为0 则可以运行程序 新增一条记录  否则关闭程序
    n = Run.select().count()
    print(n)
    if n == 0:
        now_timestmap = int(time.time())
        print(now_timestmap)
        run = Run.create(times=now_timestmap, update_time=now_timestmap)
        return True, run
    else:
        return False, None


# 更新当前程序的更新时间
def sql_update(run):
    run.update(update_time=int(time.time())).execute()

def sql_check():
    try:
        sign, run = sql_start()
    except:
        print('******出错')
        return
    if sign:
        time.sleep(10)
        sql_update(run)
    if not db.is_closed():
        print('没有关闭')
        db.close()

sql_check()