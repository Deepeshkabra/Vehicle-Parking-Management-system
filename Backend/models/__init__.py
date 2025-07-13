from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import all models to ensure they're registered with SQLAlchemy
from .user import User
from .parking_lot import ParkingLot
from .parking_spot import ParkingSpot
from .reservation import Reservation

# Export all models for easy import
__all__ = ['db', 'User', 'ParkingLot', 'ParkingSpot', 'Reservation']

def init_db(app):
    """Initialize database with the Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
