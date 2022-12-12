# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os

defaults = {
    'general': {
        'enabled': 'True',
        'owm_apikey': '',
        'owm_location': '',
        'temp_low': '4',
        'temp_high': '6',
    },
}

app_dir = os.path.dirname(__file__)
config_dir = os.path.join(app_dir, "config")
os.makedirs(config_dir, exist_ok=True)

settings_file = os.path.join(config_dir, 'config.ini')

settings = ConfigParser()
settings.read_dict(defaults)
settings.read(settings_file)


def save_settings(data):
    from scheduler import scheduler

    settings['general']['enabled'] = str(data['enabled'])
    settings['general']['owm_apikey'] = str(data['owm_apikey'])
    settings['general']['owm_location'] = str(data['owm_location'])
    settings['general']['temp_low'] = str(data['temp_low'])
    settings['general']['temp_high'] = str(data['temp_high'])
    with open(settings_file, 'w') as configfile:
        settings.write(configfile)

    if settings.get('general', 'owm_apikey') != '' and settings.get('general', 'owm_location') != '':
        scheduler.start()
