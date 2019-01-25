# Date:         Jan 24, 2019
#
# Author:       Tural Mahmudov <nima.bavari@gmail.com>
#               https://github.com/NimaBavari
#
# Description:  A simple Flask web service that performs currency conversions.
#               Here are the steps:
#               (1) Request https://openexchangerates.org/ for CZK, EUR, PLN
#               and USD;
#               (2) To keep from clogging, request only once a day and keep the
#               results in a simple JSON file;
#               (3) Perform the conversion;
#               (4) Make a clean and simple user interface.

import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '7zSogujyV0)V@KTE<!_imSi-l-t%%-4I'

APP_ID = 'df5d2ad53f3c486e88653a55f404fda6'
URL = 'https://openexchangerates.org/api/latest.json?app_id=%s' % APP_ID


def refresh_json():
    resp = requests.get(URL).json()
    rates = resp['rates']
    czk = 1 / rates['CZK']
    eur = 1 / rates['EUR']
    pln = 1 / rates['PLN']
    rate_data = {
        'CZK': czk,
        'EUR': eur,
        'PLN': pln,
        'USD': 1
    }
    with open('data.json', 'w') as out:
        json.dump(rate_data, out)


sched = BackgroundScheduler(daemon=True)
sched.add_job(refresh_json, 'interval', minutes=1440)
sched.start()


class ConversionForm(FlaskForm):
    first_val = FloatField(
        'Enter the value',
        validators=[DataRequired()]
    )
    first_unit = SelectField(
        choices=[
            ('CZK', 'CZK'),
            ('EUR', 'EUR'),
            ('PLN', 'PLN'),
            ('USD', 'USD')
        ]
    )
    second_unit = SelectField(
        choices=[
            ('CZK', 'CZK'),
            ('EUR', 'EUR'),
            ('PLN', 'PLN'),
            ('USD', 'USD')
        ]
    )
    submit = SubmitField('Convert')


@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'EnDATA Currency Converter'
    form = ConversionForm()
    result = None
    with open('data.json') as data:
        rates = json.load(data)
    if form.validate_on_submit():
        first_val = form.first_val.data
        first_unit = form.first_unit.data
        second_unit = form.second_unit.data
        result = first_val * rates[first_unit] / rates[second_unit]
    return render_template('index.html', title=title, form=form, result=result)


if __name__ == '__main__':
    app.run(debug=True)

