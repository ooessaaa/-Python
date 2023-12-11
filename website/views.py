from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Weather
from .models import City
import numpy as np
from .model_prediction import make_prediction
from . import db
import json
import string
import requests
from googletrans import Translator


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
  current_weather = ""

  if request.method =='POST':
    #Получение данных от пользователя из формы
    if (len(request.form['temperature']) < 1) or (len(request.form['humidity']) < 1) or (len(request.form['precip']) < 1) or (len(request.form['ws']) < 1) or (len(request.form['pressure']) < 1):
      flash('No Value!', category='error')
    else:
      tempc = str(request.form['temperature'])
      tempf = str((9/5)*int(request.form['temperature'])+32)
      humidity = str(request.form['humidity'])
      precip1 = str(request.form['precip'])
      os = str(int(request.form['precip'])/25.4)
      windspeed = str(request.form['ws'])
      wind = str(int(request.form['ws'])*2.237)
      sealevelpressure = str(request.form['pressure'])
      press = str(int(request.form['pressure'])*(4/3))
  
  
      #Запись переменных в список 
      x = [tempf, humidity, os, wind, press]
      #Преобразование каждого значения x в int 
      y = [eval(i) for i in x]

      #Вызов функции для предсказания погоды cо значениями y в np.array
      encoded_predictions = make_prediction(np.array([y]))

      #По значению encoded_predictions определяем c помощью decoder, какая погода
      print(encoded_predictions)
      decoder = ["clear-day", "cloudy", "partly-cloudy-day", "rain", "snow"]
      decoder2 = ["ясный день", "облачно", "переменная облачность", "дождь", "снег"]
      z = decoder[round(encoded_predictions[0])]
      z2 = decoder2[round(encoded_predictions[0])]
      current_weather = z
      
      z1 = Weather(temp=tempf,humid=humidity, precip=precip1,ws=windspeed,pressure=sealevelpressure, result = z, user_id=current_user.id)
      #Добавление в базу данных
      db.session.add(z1)
      db.session.commit()

      #Добавляем сообщение для отображения в html
      flash(("Температура:   " + tempc + "С","Влажность:   " + humidity + "%","Осадки:   " + precip1 + "мм","Скорость ветра:   " + windspeed + "м/с","Давление:   " + sealevelpressure + "мм.рт.ст", "Погода на данный момент:   " + z2), category='weather')
      # weather_images = weather_images.get(z, "по_умолчанию_если_не_найдено")
  return render_template("home.html", user=current_user, weather_images=weather_images, current_weather=current_weather)

@views.route('/weather')
def index_get():
    cities = City.query.filter_by(user_id=current_user.id).all()
    weather_data = []

    weather_images = {
        "clear-day": "Без названия (1).png",
        "cloudy": "images (1).png",
        "partly-cloudy-day": "pcloud.png",
        "rain": "rain.png",
        "snow": "images.png"
  }
    current_weather = "clear-day"

    for city in cities:
        r = get_weather_data(city.name)
        translator = Translator()
        translated = translator.translate(city.name, src='en', dest='ru')
        city_name = translated.text
        descript = translator.translate(str(r['weather'][0]['description']), src='en', dest='ru').text

        weather = {
            'city' : city_name,
            'temperature' : r['main']['temp'],
            'humidity': r['main']['humidity'],
            'pressure': r['main']['pressure'],
            'windspeed': r['wind']['speed'],
            'description' : descript.lower(),
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@views.route('/weather', methods=['POST'])
@login_required
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    print(new_city)
    translator = Translator()
    translated = translator.translate(new_city, src='ru', dest='en')
    new_city = translated.text
    new_city = new_city.lower()
    new_city = string.capwords(new_city)

    if new_city:
        existing_city = City.query.filter_by(name=new_city, user_id=current_user.id).first()
       
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            print(new_city_data)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city, user_id=current_user.id)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'Некорректное название города!'
        else:
            err_msg = 'Такой город уже есть!'

    if err_msg:
        flash(err_msg, category = 'error')
    else:
        flash('Город добавлен', category = 'success')

    return redirect(url_for('views.index_get'))

@views.route('/weather/delete/<name>')
def delete_city( name ):
    translator = Translator()
    translated = translator.translate(name, src='ru', dest='en')
    name = translated.text
    city = City.query.filter_by(name=name, user_id=current_user.id).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Успешно удален { city.name }!', category ='success')
    return redirect(url_for('views.index_get'))


def get_weather_data(city):
    print(city)    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b001f66f1c3ca44c9b559f0bea1640a1&units=metric'
    reque = requests.get(url, timeout=20)
    print(city) 
    if reque.status_code == 200:
      r = reque.json()
    else: print("fail")
    return r
    
