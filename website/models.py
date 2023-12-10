from . import db 
from flask_login import UserMixin


class Weather(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  temp = db.Column(db.Float)
  humid = db.Column(db.Float)
  precip = db.Column(db.Float)
  ws = db.Column(db.Float)
  pressure = db.Column(db.Float)
  result = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    weathers = db.relationship("Weather")

class City(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))