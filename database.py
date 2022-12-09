# -*- coding: utf-8 -*-

import atexit
import os

from peewee import Model, FloatField, TimestampField, IntegerField
from playhouse.sqliteq import SqliteQueueDatabase

# database = SqliteQueueDatabase('file::memory:?cache=shared',
database = SqliteQueueDatabase(os.path.join(os.path.dirname(__file__), "config", "db", "temperatures.db"),
                               use_gevent=False,
                               autostart=True,
                               queue_max_size=64)


@atexit.register
def _stop_worker_threads():
    database.stop()


class BaseModel(Model):
    class Meta:
        database = database


class TempLog(BaseModel):
    temperature_ext = FloatField()
    timestamp = TimestampField()
    temp_low = IntegerField()
    temp_high = IntegerField()

    class Meta:
        table_name = 'templog'
        primary_key = False


def init_db():
    database.create_tables([TempLog])
