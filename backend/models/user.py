from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_config import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship with Wallet, removed the 'dynamic' loader as it's not compatible with 'uselist=False'
    wallet = db.relationship('Wallet', back_populates='owner', uselist=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
