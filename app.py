# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
from json import dumps

from database import init_db, TempLog
from scheduler import scheduler
from config import settings
from weather import forecast
from config import save_settings

init_db()
if settings.get('general', 'owm_apikey') != '' and settings.get('general', 'owm_location') != '':
    scheduler.start()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    temps = TempLog.select(TempLog.timestamp.alias('Date'),
                           TempLog.temperature_ext.alias('TemperatureExt'),
                           TempLog.temperature_int.alias('TemperatureInt'),
                           TempLog.temp_low,
                           TempLog.temp_high,
                           TempLog.state)\
        .dicts()
    temps = list(temps)
    state = group_state(temps)

    for item in temps:
        item['Date'] = item['Date'].isoformat()

    forecasted_temps = forecast.forecast
    forecasted_temps.insert(0, {'Date': temps[-1]['Date'], 'Temperature': temps[-1]['TemperatureExt']})

    return render_template('index.html', settings=settings, data=dumps(temps), forecast=dumps(forecasted_temps),
                           state=state)


def group_state(temps):
    grouped_list = []
    item_to_add = [None, None]

    for item in temps:
        if item['state']:
            if not item_to_add[0]:
                item_to_add[0] = item['Date']
            else:
                item_to_add[1] = item['Date']
        else:
            if item_to_add[0]:
                item_to_add[1] = item['Date']
                grouped_list.append(item_to_add)
                item_to_add = [None, None]

    if item_to_add not in grouped_list and item_to_add[0] and item_to_add[1]:
        grouped_list.append(item_to_add)

    return grouped_list


@app.route('/save_settings', methods=['POST'])
def save_settings_to_file():
    data = request.get_json()
    save_settings(data)
    return redirect(url_for('main'))


if __name__ == '__main__':
    serve(app, port=80, threads=16)
