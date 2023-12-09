from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Weather
from .models import City
import numpy as np
from .model_prediction import make_prediction
from . import db
from . import db2
import json
import string
import requests
#Allows for all routes to be stored in this file
views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
 
  weather_images = {
        "clear-day": "Без названия (1).png",
        "cloudy": "images (1).png",
        "partly-cloudy-day": "pcloud.png",
        "rain": "rain.png",
        "snow": "images.png"
  }
  current_weather = "clear-day"

  if request.method =='POST':
    #Getting variables from start page that user entered 
    temp1 = str(request.form['temperature'])
    humidity = str(request.form['humidity'])
    precip1 = str(request.form['precip'])
    windspeed = str(request.form['ws'])
    sealevelpressure = str(request.form['pressure'])
    #sealevelpressure = request.form.get('pressure')

    
    if len(temp1) < 1:
      flash('No Value!', category='error')
    else:
      new_temp = Weather(temp=temp1, user_id=current_user.id)
      new_humidity = Weather(humid=humidity, user_id=current_user.id)
      new_precip = Weather(precip=precip1, user_id=current_user.id)
      new_windspeed = Weather(ws=windspeed, user_id=current_user.id)
      new_pressure = Weather(pressure=sealevelpressure, user_id=current_user.id)
      db.session.add(new_temp)
      db.session.add(new_humidity)
      db.session.add(new_precip)
      db.session.add(new_windspeed)
      db.session.add(new_pressure)
      db.session.commit()

  
    #Puts variables into list of str 
    x = [temp1, humidity, precip1, windspeed, sealevelpressure]
    #Converts each item in the x list to of int  
    y = [eval(i) for i in x]

    #Make a call to function from model_prediction.py
    #Make list y into a np.array for the model to understand 
    #Will return the prediction 
    encoded_predictions = make_prediction(np.array([y]))

    #Decoder is used to output icon name instead of number 
    decoder = ["clear-day", "cloudy", "partly-cloudy-day", "rain", "snow"]
    #Prediction number is changed from number to icon name
    z = decoder[round(encoded_predictions[0])]
    current_weather = z
    #Add to database
    z1 = Weather(result = z, user_id=current_user.id)
    db.session.add(z1)
    db.session.commit()

    #Use flash to put the prediction icon name on web page
    flash("The Weather Looks Like: " + z)
    # weather_images = weather_images.get(z, "по_умолчанию_если_не_найдено")
  return render_template("home.html", user=current_user, weather_images=weather_images, current_weather=current_weather)

@views.route('/weather')
def index_get():
    cities = City.query.all()

    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@views.route('/weather', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    print(new_city)
    new_city = new_city.lower()
    new_city = string.capwords(new_city)
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()
       
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            print(new_city_data)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)

                db2.session.add(new_city_obj)
                db2.session.commit()
            else:
                err_msg = 'That is not a valid city!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!', 'success')

    return redirect(url_for('views.index_get'))

@views.route('/weather/delete/<name>')
def delete_city( name ):
    city = City.query.filter_by(name=name).first()
    db2.session.delete(city)
    db2.session.commit()

    flash(f'Successfully deleted { city.name }!', 'success')
    return redirect(url_for('views.index_get'))


def get_weather_data(city):
    print(city)    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b001f66f1c3ca44c9b559f0bea1640a1&units=metric'
    # url = f"http://api.openweathermap.org/data/2.5/weather?appid=b001f66f1c3ca44c9b559f0bea1640a1&q={city}"
    reque = requests.get(url, timeout=20)
    print(city) 
    if reque.status_code == 200:
      r = reque.json()
    else: print("fail")
    return r
    
