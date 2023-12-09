from . import db 
from . import db2 
from flask_login import UserMixin


#Setup weather model
class Weather(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  temp = db.Column(db.Float)
  humid = db.Column(db.Float)
  precip = db.Column(db.Float)
  ws = db.Column(db.Float)
  pressure = db.Column(db.Float)
  result = db.Column(db.String)
  #User stored weather
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#Setup user model for database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #Create email where unique is true so no two users have same email 
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    weathers = db.relationship("Weather")

class City(db2.Model) :
    id = db2.Column(db2.Integer, primary_key=True)
    name = db2.Column(db2.String(50),nullable=False)