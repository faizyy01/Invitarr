from app import app
from app import db, bcrypt
from app.models import User
from os import path

if __name__ == "__main__":
    app.run(debug=False)