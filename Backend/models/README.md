# Vehicle Parking App Database Schema

## Overview
This document describes the database schema for the Vehicle Parking Management System. The system uses SQLite with SQLAlchemy ORM and supports two user roles: Admin and User.

## Database Configuration
- **Database Engine**: SQLite
- **ORM**: SQLAlchemy
- **Location**: `parking_app.db` (in project root)
- **Initialization**: Programmatic creation via `init_db.py`

## Table Definitions

### 1. Users Table (`users`)
Stores user information for both admin and regular users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(80) | UNIQUE, NOT NULL, INDEXED | User's login name |
| email | VARCHAR(120) | UNIQUE, NOT NULL, INDEXED | User's email address |
| password_hash | VARCHAR(128) | NOT NULL | Hashed password |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'user', INDEXED | User role (admin/user) |
| is_active | BOOLEAN | NOT NULL, DEFAULT True | Account status |
| first_name | VARCHAR(50) | NULLABLE | User's first name |
| last_name | VARCHAR(50) | NULLABLE | User's last name |
| phone | VARCHAR(15) | NULLABLE | User's phone number |
| created_at | DATETIME | NOT NULL, DEFAULT NOW, INDEXED | Account creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |
| last_login | DATETIME | NULLABLE | Last login timestamp |

**Constraints:**
- `CHECK (role IN ('admin', 'user'))`
- `CHECK (length(username) >= 3)`
- `CHECK (length(email) >= 5)`

**Indexes:**
- `username` (UNIQUE)
- `email` (UNIQUE)
- `role`
- `created_at`

### 2. Parking Lots Table (`parking_lots`)
Stores parking lot information and configuration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique parking lot identifier |
| prime_location_name | VARCHAR(100) | NOT NULL, INDEXED | Location name |
| address | TEXT | NOT NULL | Full address |
| pin_code | VARCHAR(10) | NOT NULL, INDEXED | Postal code |
| number_of_spots | INTEGER | NOT NULL | Total parking spots |
| price | NUMERIC(10,2) | NOT NULL | Price per hour |
| is_active | BOOLEAN | NOT NULL, DEFAULT True | Lot status |
| description | TEXT | NULLABLE | Additional description |
| operating_hours_start | TIME | NULLABLE | Opening time |
| operating_hours_end | TIME | NULLABLE | Closing time |
| created_at | DATETIME | NOT NULL, DEFAULT NOW, INDEXED | Creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |

**Constraints:**
- `CHECK (number_of_spots > 0)`
- `CHECK (price >= 0)`
- `CHECK (length(prime_location_name) >= 3)`
- `CHECK (length(pin_code) >= 6)`

**Indexes:**
- `prime_location_name`
- `pin_code`
- `created_at`

### 3. Parking Spots Table (`parking_spots`)
Stores individual parking spot information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique spot identifier |
| lot_id | INTEGER | NOT NULL, FOREIGN KEY, INDEXED | Reference to parking lot |
| spot_number | INTEGER | NOT NULL | Spot number within lot |
| status | VARCHAR(1) | NOT NULL, DEFAULT 'A', INDEXED | Spot status (A/O) |
| spot_type | VARCHAR(20) | DEFAULT 'regular' | Spot type |
| vehicle_type | VARCHAR(20) | DEFAULT '4wheeler' | Supported vehicle type |
| created_at | DATETIME | NOT NULL, DEFAULT NOW, INDEXED | Creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |

**Constraints:**
- `CHECK (status IN ('A', 'O'))` (A=Available, O=Occupied)
- `CHECK (spot_number > 0)`
- `CHECK (spot_type IN ('regular', 'handicapped', 'vip'))`
- `CHECK (vehicle_type IN ('4wheeler'))`
- `UNIQUE (lot_id, spot_number)`

**Indexes:**
- `lot_id`
- `status`
- `created_at`

**Foreign Keys:**
- `lot_id` → `parking_lots(id)` ON DELETE CASCADE

### 4. Reservations Table (`reservations`)
Stores parking reservation and booking information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique reservation identifier |
| spot_id | INTEGER | NOT NULL, FOREIGN KEY, INDEXED | Reference to parking spot |
| user_id | INTEGER | NOT NULL, FOREIGN KEY, INDEXED | Reference to user |
| parking_timestamp | DATETIME | NOT NULL, INDEXED | Parking start time |
| leaving_timestamp | DATETIME | NULLABLE, INDEXED | Parking end time |
| expected_leaving_time | DATETIME | NULLABLE | Expected departure time |
| parking_cost | NUMERIC(10,2) | DEFAULT 0.0 | Total parking cost |
| hourly_rate | NUMERIC(10,2) | NOT NULL | Rate per hour |
| vehicle_number | VARCHAR(20) | NULLABLE | Vehicle license plate |
| vehicle_model | VARCHAR(50) | NULLABLE | Vehicle model |
| vehicle_color | VARCHAR(20) | NULLABLE | Vehicle color |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active', INDEXED | Reservation status |
| remarks | TEXT | NULLABLE | Additional notes |
| created_at | DATETIME | NOT NULL, DEFAULT NOW, INDEXED | Creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |

**Constraints:**
- `CHECK (status IN ('active', 'completed', 'cancelled'))`
- `CHECK (parking_cost >= 0)`
- `CHECK (hourly_rate > 0)`
- `CHECK (leaving_timestamp IS NULL OR leaving_timestamp > parking_timestamp)`

**Indexes:**
- `spot_id`
- `user_id`
- `parking_timestamp`
- `leaving_timestamp`
- `status`
- `created_at`

**Foreign Keys:**
- `spot_id` → `parking_spots(id)` ON DELETE CASCADE
- `user_id` → `users(id)` ON DELETE CASCADE

## Relationships

### Entity Relationship Diagram
```
Users (1) ←→ (Many) Reservations
Parking Lots (1) ←→ (Many) Parking Spots
Parking Spots (1) ←→ (Many) Reservations
```

### Detailed Relationships

1. **User → Reservations** (One-to-Many)
   - A user can have multiple reservations
   - Each reservation belongs to one user
   - Cascade delete: When user is deleted, all reservations are deleted

2. **Parking Lot → Parking Spots** (One-to-Many)
   - A parking lot has multiple spots
   - Each spot belongs to one parking lot
   - Cascade delete: When parking lot is deleted, all spots are deleted

3. **Parking Spot → Reservations** (One-to-Many)
   - A spot can have multiple reservations over time
   - Each reservation is for one specific spot
   - Cascade delete: When spot is deleted, all reservations are deleted

## Business Rules

### User Management
- Only one admin user allowed in the system
- Admin user is created automatically during database initialization
- Regular users must register to access the system
- Username and email must be unique across all users

### Parking Lot Management
- Parking lots can only be deleted if all spots are available (empty)
- When a parking lot is created, spots are automatically generated
- Number of spots cannot be negative
- Price must be non-negative

### Spot Management
- Spots are automatically created when a parking lot is created
- Each spot has a unique number within its parking lot
- Spots can only be 'A' (Available) or 'O' (Occupied)
- System supports only 4-wheeler vehicles

### Reservation Management
- Users cannot select specific spots (auto-allocation)
- First available spot is assigned automatically
- Reservations calculate cost based on duration and hourly rate
- Minimum billing is 1 hour (rounded up)
- Active reservations mark spots as occupied

## Database Initialization

### Default Admin User
- **Username**: admin
- **Password**: admin123
- **Email**: admin@parkingapp.com
- **Role**: admin

### Sample Data
The system includes sample data for testing:
- 3 sample users with role 'user'
- 4 sample parking lots with different configurations
- Sample reservations with various statuses

## Usage Examples

### Initialize Database
```bash
# Create database with sample data
python init_db.py

# Create database without sample data
python init_db.py --no-sample

# Reset database
python init_db.py --reset

# Show database statistics
python init_db.py --stats
```

### Common Queries

#### Get Available Spots
```python
from models import ParkingSpot, ParkingLot

# Get all available spots
available_spots = ParkingSpot.query.filter_by(status='A').all()

# Get available spots for a specific parking lot
lot = ParkingLot.query.filter_by(id=1).first()
available_spots = lot.get_available_spots_count()
```

#### Create Reservation
```python
from models import Reservation, ParkingLot
from datetime import datetime

# Find available spot
lot = ParkingLot.query.filter_by(id=1).first()
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

#### Complete Reservation
```python
reservation = Reservation.query.filter_by(id=1).first()
if reservation.complete_reservation():
    db.session.commit()
```

## Performance Considerations

### Indexes
- All foreign keys are indexed for efficient joins
- Frequently queried columns (status, role, timestamps) are indexed
- Unique constraints on username and email for fast lookups

### Optimization Tips
- Use `db.session.bulk_insert_mappings()` for bulk operations
- Implement connection pooling for concurrent access
- Consider read replicas for reporting queries
- Use appropriate page sizes for pagination

## Security Considerations

### Password Security
- Passwords are hashed using werkzeug's security functions
- No plain text passwords stored in database
- Password complexity should be enforced at application level

### Data Validation
- All user inputs are validated at both model and application level
- SQL injection prevention through parameterized queries
- Check constraints prevent invalid data states

### Access Control
- Role-based access control implemented at application level
- Admin-only endpoints protected by middleware
- User can only access their own reservations

## Backup and Recovery

### Backup Database
```python
from models.db_utils import backup_database
backup_database(app, 'backup.db')
```

### Restore Database
```python
from models.db_utils import restore_database
restore_database(app, 'backup.db')
```

## Migration Strategy

For future schema changes:
1. Create backup before migration
2. Write migration scripts for data transformation
3. Test migrations on copy of production data
4. Implement rollback procedures
5. Monitor performance after migration

## Monitoring

### Database Statistics
Use `get_database_stats()` to monitor:
- Total users, parking lots, spots, reservations
- Active vs completed reservations
- Spot utilization rates
- User activity patterns 