import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config/user.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import db, bcrypt
from app.models import User
print(os.path.isfile("app/config/user.db"))
if os.path.isfile("app/config/user.db") is False:
    DEFAULT_USER = "admin"
    DEFAULT_PASS = "admin"
    db.create_all()
    
    try:
        hashed_password = bcrypt.generate_password_hash(DEFAULT_PASS).decode('utf-8')
        user = User(username=DEFAULT_USER, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print("Setting username and password default admin admin.")
    except Exception as e:
        print(e)
        print("Some error in setting up.")

from app import routes
