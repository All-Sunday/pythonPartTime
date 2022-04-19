# @Description:
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


def sql_start():
    now_timestmap = int(time.time())
    Run.delete().where(Run.update_time < now_timestmap - 60).execute()

    n = Run.select().count()
    if n == 0:
        now_timestmap = int(time.time())
        run = Run.create(times=now_timestmap, update_time=now_timestmap)
        return True, run
    else:
        return False, None


def sql_update(target_times):
    Run.update(update_time=int(time.time())).where(Run.times==target_times).execute()
