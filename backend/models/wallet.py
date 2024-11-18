from datetime import datetime
from database.db_config import db  

class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)  # Starting balance can be set to 0.0
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to User
    user = db.relationship('User', backref='wallet')

    def deposit(self, amount):
        """Increase balance."""
        self.balance += amount

    def withdraw(self, amount):
        """Decrease balance if sufficient funds exist."""
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "balance": self.balance,
            "date_created": self.date_created
        }
