# -*- coding: utf-8 -*-

import atexit
import os

from peewee import Model, FloatField, TimestampField, IntegerField, BooleanField
from playhouse.sqliteq import SqliteQueueDatabase
from playhouse.migrate import SqliteMigrator, migrate

# create config directories structure
app_dir = os.path.dirname(__file__)
db_dir = os.path.join(app_dir, "config", "db")
os.makedirs(db_dir, exist_ok=True)

database = SqliteQueueDatabase(os.path.join(os.path.dirname(__file__), "config", "db", "temperatures.db"),
                               use_gevent=False,
                               autostart=True,
                               queue_max_size=64)
migrator = SqliteMigrator(database)


@atexit.register
def _stop_worker_threads():
    database.stop()


class BaseModel(Model):
    class Meta:
        database = database


class TempLog(BaseModel):
    temperature_ext = FloatField(null=True)
    temperature_int = FloatField(null=True)
    timestamp = TimestampField(primary_key=True)
    temp_low = IntegerField()
    temp_high = IntegerField()
    state = BooleanField(null=True)

    class Meta:
        table_name = 'templog'


def init_db():
    database.create_tables([TempLog])
    migrate(
        migrator.add_column('templog', 'state', BooleanField(null=True)),
    )
