# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os

defaults = {
    'general': {
        'omw_apikey': '9e3ca47ce24cffe6c489db8b5f4be84f',
        'omw_location': 'Beauport, Quebec, CA',
        'temp_low': '4',
        'temp_high': '6',
    },
}

settings_file = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')

settings = ConfigParser()
settings.read_dict(defaults)
settings.read(settings_file)


def save_settings(data):
    settings['general']['enabled'] = str(data['enabled'])
    with open(settings_file, 'w') as configfile:
        settings.write(configfile)
