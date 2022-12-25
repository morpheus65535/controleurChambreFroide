# -*- coding: utf-8 -*-

import os

from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum
from datetime import datetime, timedelta

from database import TempLog
from config import settings
if 'NO_SENSOR' not in os.environ:
    from sensor import interior_temperature
if 'NO_RELAY' not in os.environ:
    from relay import relay

CONFIG = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'en',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': True,
        'use_proxy': False,
        'timeout_secs': 15,
        'max_retries': 3
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}


def get_current_temp():
    owm = OWM(settings['general']['owm_apikey'], config=CONFIG)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(settings['general']['owm_location'])
    w = observation.weather
    return w.temperature('celsius')['temp']


def log_current_temp():
    current_temp_ext = get_current_temp()
    if 'NO_SENSOR' not in os.environ:
        current_temp_int = interior_temperature.temperature
    else:
        current_temp_int = None

    if 'NO_RELAY' not in os.environ:
        current_state = relay.get_state()
    else:
        current_state = False
    TempLog.insert({TempLog.temperature_ext: current_temp_ext,
                    TempLog.temperature_int: current_temp_int,
                    TempLog.timestamp: datetime.now().timestamp(),
                    TempLog.temp_low: settings['general']['temp_low'],
                    TempLog.temp_high: settings['general']['temp_high'],
                    TempLog.state: current_state,
                    }).execute()
    TempLog.delete().where(TempLog.timestamp < (datetime.now() - timedelta(days=7))).execute()


def get_latest_logged_exterior_temp():
    last_temp = TempLog.get_or_none().order_by(TempLog.timestamp.desc())
    if last_temp:
        return last_temp.temperature_ext


class Forecast:
    def __init__(self):
        self.forecast = []

    def update_forecast(self):
        owm = OWM(settings['general']['owm_apikey'], config=CONFIG)
        mgr = owm.weather_manager()
        weathers = mgr.forecast_at_place(settings['general']['owm_location'], '3h', limit=9).forecast
        self.forecast = [{'Date': datetime.fromtimestamp(x.ref_time).isoformat(),
                          'Temperature': x.temperature('celsius')['temp']} for x in weathers]


forecast = Forecast()
