
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"
    
    def get_hashed_password(password: str) -> str:
        """
        Zamienia hasło w formie tekstowej na bezpieczny hash.
        """
        return generate_password_hash(password, method='scrypt')

    def verify_password(hashed_password: str, password: str) -> bool:
        """
        Sprawdza, czy podane hasło odpowiada hashowi.
        """
        return check_password_hash(hashed_password, password)
    
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f"Products('{self.name}', '{self.price}')"