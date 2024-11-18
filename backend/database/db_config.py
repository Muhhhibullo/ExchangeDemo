from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Initialize SQLAlchemy instance
db = SQLAlchemy()
Base = declarative_base()

def init_db(app):
    """
    Initialize the database with the Flask app.
    """
    # Configuring the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/crypto_exchange'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

