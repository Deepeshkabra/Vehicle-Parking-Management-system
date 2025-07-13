from datetime import datetime
from . import db

class ParkingSpot(db.Model):
    """Parking spot model"""
    __tablename__ = 'parking_spots'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to parking lot
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False, index=True)
    
    # Spot identification
    spot_number = db.Column(db.Integer, nullable=False)
    
    # Status: 'A' for Available, 'O' for Occupied
    status = db.Column(db.String(1), nullable=False, default='A', index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='parking_spot', lazy=True, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint("status IN ('A', 'O')", name='valid_status'),
        db.CheckConstraint("spot_number > 0", name='positive_spot_number'),
        db.UniqueConstraint('lot_id', 'spot_number', name='unique_spot_per_lot'),
    )
    
    def is_available(self):
        """Check if spot is available"""
        return self.status == 'A'
    
    def is_occupied(self):
        """Check if spot is occupied"""
        return self.status == 'O'
    
    def mark_occupied(self):
        """Mark spot as occupied"""
        self.status = 'O'
        self.updated_at = datetime.now()
    
    def mark_available(self):
        """Mark spot as available"""
        self.status = 'A'
        self.updated_at = datetime.now()
    
    def get_current_reservation(self):
        """Get current active reservation for this spot"""
        return next((r for r in self.reservations if r.is_active()), None)
    
    def get_spot_identifier(self):
        """Get spot identifier string"""
        return f"{self.parking_lot.prime_location_name}-{self.spot_number}"
    
    def to_dict(self):
        """Convert parking spot to dictionary for API responses"""
        current_reservation = self.get_current_reservation()
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'spot_number': self.spot_number,
            'status': self.status,
            'spot_type': self.spot_type,
            'vehicle_type': self.vehicle_type,
            'spot_identifier': self.get_spot_identifier(),
            'is_available': self.is_available(),
            'is_occupied': self.is_occupied(),
            'current_reservation': current_reservation.to_dict() if current_reservation else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
