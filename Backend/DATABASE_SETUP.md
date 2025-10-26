# Database Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd Backend
pip install -r requirements.txt  # After requirements.txt is created
```

### 2. Initialize Database
```bash
# Create database with sample data
python init_db.py

# Or create empty database
python init_db.py --no-sample
```

### 3. Default Login Credentials
- **Admin**: username=`admin`, password=`admin123`
- **Sample Users**: username=`john_doe`, password=`password123`

## Database Structure

### Core Tables
1. **users** - User accounts (admin/user roles)
2. **parking_lots** - Parking lot locations and pricing
3. **parking_spots** - Individual parking spaces
4. **reservations** - Parking bookings and history

### Key Relationships
- Users can have multiple reservations
- Parking lots contain multiple spots
- Spots can have multiple reservations over time

## Usage in Flask App

### 1. Import Models
```python
from models import db, User, ParkingLot, ParkingSpot, Reservation
from models import init_db
```

### 2. Initialize in App
```python
from flask import Flask
from models import init_db

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialize database
init_db(app)
```

### 3. Common Operations

#### Create User
```python
user = User(
    username='newuser',
    email='user@example.com',
    role='user'
)
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

#### Create Parking Lot
```python
lot = ParkingLot(
    prime_location_name='New Location',
    address='123 New Street',
    pin_code='123456',
    number_of_spots=25,
    price=20.00
)
db.session.add(lot)
db.session.commit()

# Auto-create spots
lot.create_parking_spots()
```

#### Make Reservation
```python
lot = ParkingLot.query.first()
spot = lot.get_next_available_spot()

if spot:
    reservation = Reservation(
        spot_id=spot.id,
        user_id=user.id,
        parking_timestamp=datetime.utcnow(),
        hourly_rate=lot.price,
        vehicle_number='ABC123'
    )
    spot.mark_occupied()
    db.session.add(reservation)
    db.session.commit()
```

## Management Commands

### Database Statistics
```bash
python init_db.py --stats
```

### Reset Database
```bash
python init_db.py --reset
```

### Backup/Restore
```python
from models.db_utils import backup_database, restore_database

# Backup
backup_database(app, 'backup.db')

# Restore
restore_database(app, 'backup.db')
```

## Files Created

- `models/__init__.py` - Database initialization
- `models/user.py` - User model
- `models/parking_lot.py` - Parking lot model
- `models/parking_spot.py` - Parking spot model
- `models/reservation.py` - Reservation model
- `models/db_utils.py` - Database utilities
- `models/README.md` - Detailed documentation
- `init_db.py` - Database setup script

## Next Steps

1. Create Flask routes for API endpoints
2. Set up authentication middleware
3. Implement business logic
4. Add Redis caching
5. Set up Celery for background jobs

This database schema is ready for the Vehicle Parking App and follows all the requirements specified in the project rules. 