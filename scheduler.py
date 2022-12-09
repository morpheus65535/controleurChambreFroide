# -*- coding: utf-8 -*-
import os

import tzlocal

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from weather import log_current_temp, forecast
if 'NO_SENSOR' not in os.environ:
    from sensor import interior_temperature


class Scheduler:

    def __init__(self):
        self.aps_scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))

        self.aps_scheduler.add_job(log_current_temp, IntervalTrigger(minutes=15), max_instances=1, id='log_temp')
        self.aps_scheduler.add_job(forecast.update_forecast, IntervalTrigger(minutes=15), max_instances=1,
                                   id='forecast')
        if 'NO_SENSOR' not in os.environ:
            self.aps_scheduler.add_job(interior_temperature.get_temperature_int, IntervalTrigger(minutes=1),
                                       max_instances=1, id='temp_int')

    def start(self):
        self.aps_scheduler.start()

    @staticmethod
    def run_once():
        scheduler.aps_scheduler.modify_job(job_id='log_temp', next_run_time=datetime.now())
        scheduler.aps_scheduler.modify_job(job_id='forecast', next_run_time=datetime.now())
        if 'NO_SENSOR' not in os.environ:
            scheduler.aps_scheduler.modify_job(job_id='temp_int', next_run_time=datetime.now())


scheduler = Scheduler()
