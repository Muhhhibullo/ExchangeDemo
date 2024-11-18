from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import db
from models.order import Order

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('orders.user_id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('orders.user_id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Relationships
    buyer = db.relationship('Order', back_populates='trades_buyer', foreign_keys=[buyer_id])
    seller = db.relationship('Order', back_populates='trades_seller', foreign_keys=[seller_id])

    def to_dict(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "price": self.price,
            "amount": self.amount,
        }
