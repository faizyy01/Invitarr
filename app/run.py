from app import app
from app import db, bcrypt
from app.models import User
from os import path
'''
if path.exists("app.config.app.db") is False:
    db.create_all()
    try:
        hashed_password = bcrypt.generate_password_hash(DEFAULT_PASS).decode('utf-8')
        user = User(username=DEFAULT_USER, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    except:
        print("Some error in setting up.")
'''
if __name__ == "__main__":
    app.run(debug=True)
