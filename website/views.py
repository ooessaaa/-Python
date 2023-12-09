from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Weather
import numpy as np
from .model_prediction import make_prediction
from . import db
import json
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

    # weather_images = {
    # "clear-day": "Без названия (1).png",
    # "cloudy": "images (1).png",
    # "partly-cloudy-day": "pcloud.png",
    # "rain": "rain.png",
    # "snow": "images.png"
    # }

    # "clear-day": "C:\\Users\\ACER\\Desktop\\WeatherPredictionSystem-main\\website\\static\\image\\Без названия (1).png",
    # "cloudy": "C:/Users/ACER/Desktop/WeatherPredictionSystem-main/website/images (1).png",
    # "partly-cloudy-day": "C:/Users/ACER/Desktop/WeatherPredictionSystem-main/website/pcloud.png",
    # "rain": "C:/Users/ACER/Desktop/WeatherPredictionSystem-main/website/rain.png",
    # "snow": "C:/Users/ACER/Desktop/WeatherPredictionSystem-main/website/images.png"
    #Выбираем соответствующее изображение на основе предсказанной погоды
    # weather_image = weather_images.get(z, "по_умолчанию_если_не_найдено")

  # return render_template("home.html", user=current_user, weather_images=weather_images, current_weather=current_weather)
