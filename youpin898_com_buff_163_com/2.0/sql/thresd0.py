# @Description: peewee数据库连接池
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/14 15:02
# @File : thresd.py


from peewee import *
import time
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from config import Config

# db = MySQLDatabase("c_go", host="124.221.131.73", port=3306, user="c_go", passwd="tfTyYHEGNxRAJPAt")



class RetryMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryMySQLDatabase._instance:
            cfg = Config('peewee.cfg')
            RetryMySQLDatabase._instance = RetryMySQLDatabase(
                cfg.get('db_name', 'aaabb'),
                max_connections=8,
                stale_timeout=300,
                host=cfg.get('db_host', '127.0.0.1'),
                user=cfg.get('db_user', 'root'),
                password=cfg.get('db_pwd', '123'),
                port=cfg.get('db_port', 3306)
            )
        return RetryMySQLDatabase._instance

class BaseModel(Model):
    class Meta:
        database = RetryMySQLDatabase.get_db_instance()


class Record(BaseModel):
    name = CharField()
    yid = CharField()
    price1 = CharField()
    price2 = CharField()
    msg = CharField()
    mode = CharField()
    update_times = IntegerField()
    state = IntegerField()

    class Meta:
        table_name = 'record'


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
    Run.update(update_time=int(time.time())).where(Run.times == target_times).execute()


def query():
    # max_id = fn.Max(Record.id)
    # print(max_id)
    # Record2 = Record.alias()
    # res = Record.select().where(Record.update_times >= int(time.time()) - 10)
    # res = Record.select().where(Record.id == fn.Max(Record.id))  # 不能直接在where用fn函数
    # res = Record.select().join(Record2, on=(Record2.id == Record.id)).where(Record.update_times >= int(time.time()) - 10)

    sub_query = Record.select(fn.Max(Record.id))
    res = Record.select().where((Record.update_times >= int(time.time()) - 10) & (Record.id == sub_query))
    # print(res.id)
    # print(res.name)
    # print(len(res))
    if len(res) == 0:
        return None
    else:
        # for r in res:
        #     print(r.id, r.name, r.yid,r.price1)
        return res[0]


def update(res, s):
    res.state = s
    res.save()

def insert(res):
    # Record.create(name=res[0], yid=str(res[1]), price1=str(res[2]), price2=str(res[3]), msg=res[4], mode=res[5],
    #               update_times=int(time.time()), state=0)
    res = Record(name=res[0], yid=str(res[1]), price1=str(res[2]), price2=str(res[3]), msg=res[4], mode=res[5],
                 update_times=int(time.time()), state=0)
    r = res.save()
    time.sleep(5)
    # print(r)
    # print('ssssss')
    return r

# insert(['摩托手套（★） | 薄荷 (崭新出厂)', '55916', 88888.0, 85555.0, '摩托手套（★） | 薄荷 (崭新出厂) 售价为85555.0，buff为86666\n', '2'])
# # print(timeit('query()', 'from __main__ import query', number=1))
# res = query()
# print(res, type(res))
# if res is not None:
#     print('u')
#     update(res, 1)


# if not db.is_closed():
#     db.close()
#     print(db.is_closed())
#     print('close')
