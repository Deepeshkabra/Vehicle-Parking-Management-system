from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    """User model for regular users"""

    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User identification
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # User role and status
    role = db.Column(db.String(20), nullable=False, default="user", index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Additional user information
    phone = db.Column(db.String(15))

    # Timestamps
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, index=True
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    last_login = db.Column(db.DateTime)

    # Relationships
    reservations = db.relationship(
        "Reservation", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        db.CheckConstraint("role IN ('user', 'admin')", name="valid_role"),
    )

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary for API responses"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
