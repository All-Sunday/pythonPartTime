from peewee import *
import time
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

# peewee 线程池
class RetryMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryMySQLDatabase._instance:
            RetryMySQLDatabase._instance = RetryMySQLDatabase(
                'c_go',
                max_connections=8,
                stale_timeout=300,
                host='124.221.131.73',
                user='c_go',
                password='tfTyYHEGNxRAJPAt',
                port=3306
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
    id1 = CharField()
    id2 = CharField()
    msg = CharField()
    mode = CharField()
    update_times = IntegerField()
    state = IntegerField()

    class Meta:
        table_name = 'record'


def query(time_gap, status):
    sub_query = Record.select(fn.Max(Record.id))
    res = Record.select().where(
        (Record.state == status) & (Record.update_times >= int(time.time()) - time_gap) & (Record.id == sub_query))

    if len(res) == 0:
        return None
    else:
        return res[0]


def orderp(times):  # 是否开始处理
    res = Record.get(Record.update_times == times)

    return False if res.state == 0 else True


def update(res, s):
    res.state = s
    res.save()


def insert(res):
    res = Record(name=res[0], yid=str(res[1]), price1=str(res[2]), price2=str(res[3]), id1=str(res[4]), id2=str(res[5]),
                 msg=res[6], mode=res[7], update_times=res[8], state=0)
    r = res.save()
    return r
