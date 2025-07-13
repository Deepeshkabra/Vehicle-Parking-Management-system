"""
Database utility functions for the Vehicle Parking App
"""
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from . import db
from .user import User
from .parking_lot import ParkingLot
from .parking_spot import ParkingSpot
from .reservation import Reservation

def create_database(app):
    """Create database tables and initialize with default data"""
    with app.app_context():
        # Drop all tables if they exist (for development)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        
        # Create sample data (optional, for testing)
        create_sample_data()
        
        print("Database created successfully!")


def create_sample_data():
    """Create sample data for testing purposes"""
    # Create sample users
    create_sample_users()
    
    # Create sample parking lots
    create_sample_parking_lots()
    
    # Create sample reservations
    create_sample_reservations()
    
    print("Sample data created successfully!")

def create_sample_users():
    """Create sample users for testing"""
    sample_users = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1234567891'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+1234567892'
        },
        {
            'username': 'mike_johnson',
            'email': 'mike@example.com',
            'password': 'password123',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'phone': '+1234567893'
        }
    ]
    
    for user_data in sample_users:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone']
            )
            db.session.add(user)
    
    db.session.commit()

def create_sample_parking_lots():
    """Create sample parking lots for testing"""
    sample_lots = [
        {
            'prime_location_name': 'Downtown Central Plaza',
            'address': '123 Main Street, Downtown District',
            'pin_code': '123456',
            'number_of_spots': 50,
            'price': 25.00,
            'description': 'Prime downtown location with 24/7 security',
            'operating_hours_start': '06:00',
            'operating_hours_end': '22:00'
        },
        {
            'prime_location_name': 'Business Park North',
            'address': '456 Business Avenue, North Zone',
            'pin_code': '123457',
            'number_of_spots': 30,
            'price': 20.00,
            'description': 'Convenient parking for business district',
            'operating_hours_start': '07:00',
            'operating_hours_end': '21:00'
        },
        {
            'prime_location_name': 'Shopping Mall East',
            'address': '789 Shopping Street, East Side',
            'pin_code': '123458',
            'number_of_spots': 75,
            'price': 15.00,
            'description': 'Large parking area for shopping center',
            'operating_hours_start': '08:00',
            'operating_hours_end': '23:00'
        },
        {
            'prime_location_name': 'Airport Terminal',
            'address': '999 Airport Road, Terminal Building',
            'pin_code': '123459',
            'number_of_spots': 100,
            'price': 35.00,
            'description': 'Premium airport parking with shuttle service',
            'operating_hours_start': '00:00',
            'operating_hours_end': '23:59'
        }
    ]
    
    for lot_data in sample_lots:
        if not ParkingLot.query.filter_by(prime_location_name=lot_data['prime_location_name']).first():
            from datetime import time
            
            lot = ParkingLot(
                prime_location_name=lot_data['prime_location_name'],
                address=lot_data['address'],
                pin_code=lot_data['pin_code'],
                number_of_spots=lot_data['number_of_spots'],
                price=lot_data['price'],
                description=lot_data['description'],
                operating_hours_start=time.fromisoformat(lot_data['operating_hours_start']),
                operating_hours_end=time.fromisoformat(lot_data['operating_hours_end'])
            )
            db.session.add(lot)
            db.session.commit()
            
            # Create parking spots for this lot
            lot.create_parking_spots()

def create_sample_reservations():
    """Create sample reservations for testing"""
    # Get some users and parking spots
    users = User.query.filter_by(role='user').limit(3).all()
    parking_lots = ParkingLot.query.all()
    
    if not users or not parking_lots:
        return
    
    sample_reservations = [
        {
            'user_id': users[0].id,
            'parking_timestamp': datetime.utcnow() - timedelta(hours=2),
            'leaving_timestamp': datetime.utcnow() - timedelta(hours=1),
            'vehicle_number': 'ABC123',
            'vehicle_model': 'Toyota Camry',
            'vehicle_color': 'Blue',
            'status': 'completed'
        },
        {
            'user_id': users[1].id,
            'parking_timestamp': datetime.utcnow() - timedelta(hours=1),
            'leaving_timestamp': None,
            'vehicle_number': 'XYZ789',
            'vehicle_model': 'Honda Civic',
            'vehicle_color': 'Red',
            'status': 'active'
        },
        {
            'user_id': users[2].id,
            'parking_timestamp': datetime.utcnow() - timedelta(days=1),
            'leaving_timestamp': datetime.utcnow() - timedelta(days=1) + timedelta(hours=3),
            'vehicle_number': 'DEF456',
            'vehicle_model': 'Ford Focus',
            'vehicle_color': 'White',
            'status': 'completed'
        }
    ]
    
    for i, reservation_data in enumerate(sample_reservations):
        # Get available spot from different parking lots
        lot = parking_lots[i % len(parking_lots)]
        available_spot = lot.get_next_available_spot()
        
        if available_spot:
            reservation = Reservation(
                spot_id=available_spot.id,
                user_id=reservation_data['user_id'],
                parking_timestamp=reservation_data['parking_timestamp'],
                leaving_timestamp=reservation_data['leaving_timestamp'],
                vehicle_number=reservation_data['vehicle_number'],
                vehicle_model=reservation_data['vehicle_model'],
                vehicle_color=reservation_data['vehicle_color'],
                status=reservation_data['status'],
                hourly_rate=lot.price
            )
            
            # Calculate cost for completed reservations
            if reservation.leaving_timestamp:
                reservation.parking_cost = reservation.calculate_cost()
            
            # Mark spot as occupied if reservation is active
            if reservation_data['status'] == 'active':
                available_spot.mark_occupied()
            
            db.session.add(reservation)
    
    db.session.commit()

def reset_database(app):
    """Reset database (drop and recreate)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully!")

def get_database_stats(app):
    """Get database statistics"""
    with app.app_context():
        stats = {
            'total_users': User.query.count(),
            'admin_users': User.query.filter_by(role='admin').count(),
            'regular_users': User.query.filter_by(role='user').count(),
            'total_parking_lots': ParkingLot.query.count(),
            'active_parking_lots': ParkingLot.query.filter_by(is_active=True).count(),
            'total_parking_spots': ParkingSpot.query.count(),
            'available_spots': ParkingSpot.query.filter_by(status='A').count(),
            'occupied_spots': ParkingSpot.query.filter_by(status='O').count(),
            'total_reservations': Reservation.query.count(),
            'active_reservations': Reservation.query.filter_by(status='active').count(),
            'completed_reservations': Reservation.query.filter_by(status='completed').count(),
            'cancelled_reservations': Reservation.query.filter_by(status='cancelled').count()
        }
        return stats

def backup_database(app, backup_path):
    """Create a backup of the database"""
    import shutil
    import os
    
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
            print(f"Database backed up to {backup_path}")
            return True
        return False

def restore_database(app, backup_path):
    """Restore database from backup"""
    import shutil
    import os
    
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, db_path)
            print(f"Database restored from {backup_path}")
            return True
        return False 