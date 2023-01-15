# -*- coding: utf-8 -*-
import os

import tzlocal
import contextlib

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers import SchedulerAlreadyRunningError

from weather import log_current_temp, forecast
if 'NO_SENSOR' not in os.environ:
    from sensor import interior_temperature
if 'NO_RELAY' not in os.environ:
    from relay import set_required_relay_state


class Scheduler:

    def __init__(self):
        self.aps_scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))

    def configure(self):
        self.aps_scheduler.add_job(log_current_temp, IntervalTrigger(minutes=15), max_instances=1, id='log_temp',
                                   replace_existing=True)
        self.aps_scheduler.add_job(forecast.update_forecast, IntervalTrigger(minutes=15), max_instances=1,
                                   id='forecast', replace_existing=True)
        if 'NO_SENSOR' not in os.environ:
            self.aps_scheduler.add_job(interior_temperature.get_temperature_int, IntervalTrigger(minutes=1),
                                       max_instances=1, id='temp_int', replace_existing=True)
        if 'NO_RELAY' not in os.environ:
            self.aps_scheduler.add_job(set_required_relay_state, IntervalTrigger(minutes=1),
                                       max_instances=1, id='set_relay', replace_existing=True)

    def start(self):
        self.configure()
        with contextlib.suppress(SchedulerAlreadyRunningError):
            self.aps_scheduler.start()
        self.run_once()

    @staticmethod
    def run_once():
        scheduler.aps_scheduler.modify_job(job_id='log_temp', next_run_time=datetime.now())
        scheduler.aps_scheduler.modify_job(job_id='forecast', next_run_time=datetime.now())
        if 'NO_SENSOR' not in os.environ:
            scheduler.aps_scheduler.modify_job(job_id='temp_int', next_run_time=datetime.now())
        if 'NO_RELAY' not in os.environ:
            scheduler.aps_scheduler.modify_job(job_id='set_relay', next_run_time=datetime.now())


scheduler = Scheduler()
