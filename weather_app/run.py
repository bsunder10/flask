from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import requests, json

api_key = '11b7ee2e8a78f34df5e2c272ae093e86'
base_url = "http://api.openweathermap.org/data/2.5/weather?"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ASKING'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city.db'
db = SQLAlchemy(app)


# **********************************************
# Form
class CityName(FlaskForm):
    cit_nam = StringField('City Name')
    submit = SubmitField('Search')

    def validate_cit_nam(self, cit_name):
        cit = City.query.filter_by(city=cit_name.data).first()
        if cit:
            raise ValidationError('City already present')


# **********************************************
# Model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), unique=True, nullable=False)
    temperature = db.Column(db.String(20), nullable=False)
    pressure = db.Column(db.String(20), nullable=False)
    humidity = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.city


# ***********************************************
# Getting the weather
def add_city(cit):
    complete_url = base_url + 'appid=' + api_key + '&q=' + cit
    responce = requests.get(complete_url)
    x = responce.json()

    if x["cod"] != '404':
        y = x['main']
        temp = y['temp']
        press = y['pressure']
        hum = y['humidity']
        z = x['weather']
        des = z[0]['description']

        ad = City(city=cit, temperature=int(temp) - 273.15, pressure=press, humidity=hum, description=des)
        db.session.add(ad)
        db.session.commit()
    else:
        flash('Could not find the city')
        return redirect(url_for('home'))


@app.route('/', methods=['POST', 'GET'])
def home():
    form = CityName()
    if form.validate_on_submit():
        if form.cit_nam.data:
            add_city(form.cit_nam.data)
    cities = City.query.all()
    return render_template('home.html', form=form, cities=cities)


if __name__ == '__main__':
    app.run(debug=True)
