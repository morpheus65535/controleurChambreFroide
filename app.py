# -*- coding: utf-8 -*-

from flask import Flask, render_template
from waitress import serve
from datetime import datetime, timedelta
from json import dumps

from database import init_db, TempLog
from scheduler import scheduler
from config import settings
from weather import forecast

init_db()
scheduler.start()

# generate first temperature logging to show data in graphs ASAP
scheduler.run_once()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    temps = TempLog.select(TempLog.timestamp.alias('Date'),
                           TempLog.temperature_ext.alias('TemperatureExt'),
                           TempLog.temperature_int.alias('TemperatureInt'),
                           TempLog.temp_low,
                           TempLog.temp_high)\
        .dicts()
    for item in temps:
        item['Date'] = item['Date'].isoformat()

    temps = list(temps)

    forecasted_temps = forecast.forecast
    if forecasted_temps:
        forecasted_temps.insert(0, {'Date': temps[-1]['Date'], 'Temperature': temps[-1]['TemperatureExt']})

    return render_template('index.html', settings=settings, data=dumps(temps), forecast=dumps(forecasted_temps))


if __name__ == '__main__':
    serve(app, port=80, threads=16)
