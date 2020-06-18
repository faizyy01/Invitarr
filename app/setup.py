from app import db, bcrypt
from app.models import User

DEFAULT_USER = "admin"
DEFAULT_PASS = "admin"
db.create_all()

try:
    hashed_password = bcrypt.generate_password_hash(DEFAULT_PASS).decode('utf-8')
    user = User(username=DEFAULT_USER, password=hashed_password)
    db.session.add(user)
    db.session.commit()
except:
    print("Some error in setting up.")
