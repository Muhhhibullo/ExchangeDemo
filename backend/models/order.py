from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import Base
from database.db_config import db

# Delayed import of Trade model
def get_trade_model():
    from models.trade import Trade
    return Trade

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Relationships with custom backref names
    trades_buyer = db.relationship('Trade', back_populates='buyer', foreign_keys='Trade.buyer_id', lazy='dynamic')
    trades_seller = db.relationship('Trade', back_populates='seller', foreign_keys='Trade.seller_id', lazy='dynamic')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "price": self.price,
            "amount": self.amount,
        }
