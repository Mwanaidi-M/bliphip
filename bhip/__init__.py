from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

# FLASK APP INITIALIZATION
my_app = Flask(__name__)
my_app.config.from_object(Config)

# DB INITIALIZATION
my_db = SQLAlchemy(my_app)

# FLASK MIGRATE INITIALIZATION
my_migrate = Migrate(my_app, my_db)

# FLASK LOGIN INITIALIZATION
my_login = LoginManager(my_app)
my_login.login_view = 'account_login'

# round import of routes & models.py file
from bhip import routes, models
