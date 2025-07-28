from datetime import datetime
from . import db


class ParkingLot(db.Model):
    """Parking lot model"""

    __tablename__ = "parking_lots"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Location information
    prime_location_name = db.Column(db.String(100), nullable=False, index=True)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False, index=True)

    # Parking lot details
    number_of_spots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price per hour

    # Status and availability
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Additional details
    description = db.Column(db.Text)
    operating_hours_start = db.Column(db.Time)
    operating_hours_end = db.Column(db.Time)

    # Timestamps
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, index=True
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    # Relationships
    parking_spots = db.relationship(
        "ParkingSpot", backref="parking_lot", lazy=True, cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        db.CheckConstraint("number_of_spots > 0", name="positive_spots"),
        db.CheckConstraint("price >= 0", name="non_negative_price"),
    )

    def get_available_spots_count(self):
        """Get count of available parking spots"""
        return len([spot for spot in self.parking_spots if spot.status == "A"])

    def get_occupied_spots_count(self):
        """Get count of occupied parking spots"""
        return len([spot for spot in self.parking_spots if spot.status == "O"])

    def has_available_spots(self):
        """Check if parking lot has available spots"""
        return self.get_available_spots_count() > 0

    def is_empty(self):
        """Check if all spots are empty (available)"""
        return self.get_occupied_spots_count() == 0

    def get_next_available_spot(self):
        """Get the next available parking spot"""
        for spot in self.parking_spots:
            if spot.status == "A":
                return spot
        return None

    def create_parking_spots(self):
        """Create parking spots based on number_of_spots"""
        from .parking_spot import ParkingSpot

        # Clear existing spots
        ParkingSpot.query.filter_by(lot_id=self.id).delete()

        # Create new spots
        for i in range(1, self.number_of_spots + 1):
            spot = ParkingSpot(lot_id=self.id, spot_number=i, status="A")
            db.session.add(spot)

        db.session.commit()

    def to_dict(self):
        """Convert parking lot to dictionary for API responses"""
        return {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "address": self.address,
            "pin_code": self.pin_code,
            "number_of_spots": self.number_of_spots,
            "price": float(self.price),
            "is_active": self.is_active,
            "description": self.description,
            "operating_hours_start": (
                self.operating_hours_start.strftime("%H:%M")
                if self.operating_hours_start
                else None
            ),
            "operating_hours_end": (
                self.operating_hours_end.strftime("%H:%M")
                if self.operating_hours_end
                else None
            ),
            "available_spots": self.get_available_spots_count(),
            "occupied_spots": self.get_occupied_spots_count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
