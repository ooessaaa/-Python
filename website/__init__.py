from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'database.db'
db2 = SQLAlchemy()


def create_app():
  #Initialize Flask
  app = Flask(__name__)
  #Encryption for cookies and web data
  app.config['SECRET_KEY'] = 'qwertyuiop'
  #Location of database
  app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///database.db'
  #Initialize database
  # Suppress deprecation warnings
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)


  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
  app.config['SECRET_KEY'] = 'thisisasecret'
  db2.init_app(app)

  from .views import views
  from .auth import auth 

  #Register blueprints with no prefix
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User
  with app.app_context():
    db.create_all()

  with app.app_context():
    db2.create_all()

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  #Tells flask how we load a user
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app 

