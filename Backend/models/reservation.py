from datetime import datetime, timedelta
from . import db

class Reservation(db.Model):
    """Reservation model for parking bookings"""
    __tablename__ = 'reservations'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Reservation timing
    parking_timestamp = db.Column(db.DateTime, nullable=False, index=True)
    leaving_timestamp = db.Column(db.DateTime, index=True)
    expected_leaving_time = db.Column(db.DateTime)
    
    # Cost and payment
    parking_cost = db.Column(db.Numeric(10, 2), default=0.0)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Vehicle details
    vehicle_number = db.Column(db.String(20))
    vehicle_model = db.Column(db.String(50))
    vehicle_color = db.Column(db.String(20))
    
    # Reservation status
    status = db.Column(db.String(20), nullable=False, default='active', index=True)
    
    # Additional details
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint("status IN ('active', 'completed', 'cancelled')", name='valid_status'),
        db.CheckConstraint("parking_cost >= 0", name='non_negative_cost'),
        db.CheckConstraint("hourly_rate > 0", name='positive_hourly_rate'),
        db.CheckConstraint("leaving_timestamp IS NULL OR leaving_timestamp > parking_timestamp", name='valid_leaving_time'),
    )
    
    def is_active(self):
        """Check if reservation is active"""
        return self.status == 'active' and self.leaving_timestamp is None
    
    def is_completed(self):
        """Check if reservation is completed"""
        return self.status == 'completed' and self.leaving_timestamp is not None
    
    def calculate_duration_hours(self):
        """Calculate parking duration in hours"""
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            return max(1, duration.total_seconds() / 3600)  # Minimum 1 hour
        return 0
    
    def calculate_cost(self):
        """Calculate parking cost based on duration"""
        if self.leaving_timestamp:
            duration_hours = self.calculate_duration_hours()
            # Round up to nearest hour
            import math
            rounded_hours = math.ceil(duration_hours)
            return float(self.hourly_rate) * rounded_hours
        return 0.0
    
    def complete_reservation(self):
        """Complete the reservation and calculate final cost"""
        if self.is_active():
            self.leaving_timestamp = datetime.utcnow()
            self.parking_cost = self.calculate_cost()
            self.status = 'completed'
            self.updated_at = datetime.utcnow()
            
            # Mark parking spot as available
            self.parking_spot.mark_available()
            
            return True
        return False
    
    def cancel_reservation(self):
        """Cancel the reservation"""
        if self.is_active():
            self.status = 'cancelled'
            self.updated_at = datetime.utcnow()
            
            # Mark parking spot as available
            self.parking_spot.mark_available()
            
            return True
        return False
    
    def get_parking_duration_str(self):
        """Get formatted parking duration string"""
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            return f"{hours}h {minutes}m"
        elif self.is_active():
            duration = datetime.utcnow() - self.parking_timestamp
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            return f"{hours}h {minutes}m (ongoing)"
        return "N/A"
    
    def is_overdue(self):
        """Check if reservation is overdue (past expected leaving time)"""
        if self.is_active() and self.expected_leaving_time:
            return datetime.utcnow() > self.expected_leaving_time
        return False
    
    def to_dict(self):
        """Convert reservation to dictionary for API responses"""
        return {
            'id': self.id,
            'spot_id': self.spot_id,
            'user_id': self.user_id,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'expected_leaving_time': self.expected_leaving_time.isoformat() if self.expected_leaving_time else None,
            'parking_cost': float(self.parking_cost),
            'hourly_rate': float(self.hourly_rate),
            'vehicle_number': self.vehicle_number,
            'vehicle_model': self.vehicle_model,
            'vehicle_color': self.vehicle_color,
            'status': self.status,
            'remarks': self.remarks,
            'duration_str': self.get_parking_duration_str(),
            'is_active': self.is_active(),
            'is_completed': self.is_completed(),
            'is_overdue': self.is_overdue(),
            'spot_identifier': self.parking_spot.get_spot_identifier() if self.parking_spot else None,
            'lot_name': self.parking_spot.parking_lot.prime_location_name if self.parking_spot else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_csv_dict(self):
        """Convert reservation to dictionary for CSV export"""
        return {
            'reservation_id': self.id,
            'slot_id': self.parking_spot.parking_lot.id if self.parking_spot else None,
            'spot_id': self.spot_id,
            'spot_number': self.parking_spot.spot_number if self.parking_spot else None,
            'lot_name': self.parking_spot.parking_lot.prime_location_name if self.parking_spot else None,
            'vehicle_number': self.vehicle_number,
            'parking_timestamp': self.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.leaving_timestamp else None,
            'duration': self.get_parking_duration_str(),
            'cost': float(self.parking_cost),
            'status': self.status,
            'remarks': self.remarks or ''
        }
    