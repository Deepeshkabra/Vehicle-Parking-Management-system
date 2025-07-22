"""
Reservation validation schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum
from .base import BaseSchema, TimestampMixin, validate_vehicle_number

class ReservationStatus(str, Enum):
    """Reservation status enumeration"""
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class ReservationBase(BaseSchema):
    """Base reservation schema"""
    spot_id: int = Field(..., gt=0, description="Parking spot ID")
    expected_leaving_time: Optional[datetime] = Field(None, description="Expected departure time")
    vehicle_number: Optional[str] = Field(None, max_length=20, description="Vehicle license plate")
    vehicle_model: Optional[str] = Field(None, max_length=50, description="Vehicle model")
    vehicle_color: Optional[str] = Field(None, max_length=20, description="Vehicle color")
    remarks: Optional[str] = Field(None, max_length=500, description="Additional remarks")
    
    @field_validator('expected_leaving_time')
    def validate_expected_leaving_time(cls, v):
        if v is not None and v <= datetime.utcnow():
            raise ValueError('Expected leaving time must be in the future')
        return v
    
    @field_validator('vehicle_number')
    def validate_vehicle_number_format(cls, v):
        if v:
            return validate_vehicle_number(v)
        return v
    
    @field_validator('vehicle_model')
    def validate_vehicle_model(cls, v):
        if v:
            return v.strip()
        return v
    
    @field_validator('vehicle_color')
    def validate_vehicle_color(cls, v):
        if v:
            return v.strip()
        return v

class ReservationCreate(ReservationBase):
    """Schema for creating reservations"""
    
    class Config:
        schema_extra = {
            "example": {
                "spot_id": 1,
                "expected_leaving_time": "2024-01-15T18:00:00",
                "vehicle_number": "ABC123",
                "vehicle_model": "Toyota Camry",
                "vehicle_color": "Blue",
                "remarks": "Visiting for business meeting"
            }
        }

class ReservationUpdate(BaseSchema):
    """Schema for updating reservations"""
    expected_leaving_time: Optional[datetime] = Field(None, description="Expected departure time")
    vehicle_number: Optional[str] = Field(None, max_length=20, description="Vehicle license plate")
    vehicle_model: Optional[str] = Field(None, max_length=50, description="Vehicle model")
    vehicle_color: Optional[str] = Field(None, max_length=20, description="Vehicle color")
    remarks: Optional[str] = Field(None, max_length=500, description="Additional remarks")
    
    @field_validator('expected_leaving_time')
    def validate_expected_leaving_time(cls, v):
        if v is not None and v <= datetime.utcnow():
            raise ValueError('Expected leaving time must be in the future')
        return v
    
    @field_validator('vehicle_number')
    def validate_vehicle_number_format(cls, v):
        if v:
            return validate_vehicle_number(v)
        return v

class ReservationComplete(BaseSchema):
    """Schema for completing reservations"""
    leaving_timestamp: Optional[datetime] = Field(None, description="Actual leaving time")
    remarks: Optional[str] = Field(None, max_length=500, description="Completion remarks")
    
    @field_validator('leaving_timestamp')
    def validate_leaving_timestamp(cls, v):
        if v is not None and v > datetime.utcnow():
            raise ValueError('Leaving time cannot be in the future')
        return v

class ReservationCancel(BaseSchema):
    """Schema for cancelling reservations"""
    reason: Optional[str] = Field(None, max_length=500, description="Cancellation reason")

class ReservationResponse(ReservationBase, TimestampMixin):
    """Schema for reservation API responses"""
    id: int
    user_id: int
    parking_timestamp: datetime
    leaving_timestamp: Optional[datetime] = None
    parking_cost: Decimal
    hourly_rate: Decimal
    status: ReservationStatus
    duration_str: str = Field(..., description="Duration string")
    is_active: bool
    is_completed: bool
    is_overdue: bool
    spot_identifier: Optional[str] = Field(None, description="Spot identifier")
    lot_name: Optional[str] = Field(None, description="Parking lot name")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "spot_id": 1,
                "parking_timestamp": "2024-01-15T10:00:00",
                "leaving_timestamp": None,
                "expected_leaving_time": "2024-01-15T18:00:00",
                "parking_cost": 0.00,
                "hourly_rate": 25.00,
                "vehicle_number": "ABC123",
                "vehicle_model": "Toyota Camry",
                "vehicle_color": "Blue",
                "status": "active",
                "remarks": "Visiting for business meeting",
                "duration_str": "2h 30m (ongoing)",
                "is_active": True,
                "is_completed": False,
                "is_overdue": False,
                "spot_identifier": "Downtown Central Plaza-1",
                "lot_name": "Downtown Central Plaza",
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }

class ReservationList(BaseSchema):
    """Schema for reservation list responses"""
    reservations: List[ReservationResponse]
    total: int
    page: int
    per_page: int

class ReservationFilter(BaseSchema):
    """Schema for reservation filtering"""
    user_id: Optional[int] = Field(None, gt=0, description="Filter by user")
    spot_id: Optional[int] = Field(None, gt=0, description="Filter by spot")
    status: Optional[ReservationStatus] = Field(None, description="Filter by status")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")
    
    @field_validator('date_to')
    def validate_date_range(cls, v, values):
        if v is not None and 'date_from' in values and values['date_from'] is not None:
            if v <= values['date_from']:
                raise ValueError('End date must be after start date')
        return v

class ReservationCSV(BaseSchema):
    """Schema for CSV export of reservations"""
    reservation_id: int
    slot_id: Optional[int] = None
    spot_id: int
    spot_number: Optional[int] = None
    lot_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    parking_timestamp: Optional[str] = None
    leaving_timestamp: Optional[str] = None
    duration: str
    cost: Decimal
    status: str
    remarks: str

class ReservationStats(BaseSchema):
    """Schema for reservation statistics"""
    total_reservations: int
    active_reservations: int
    completed_reservations: int
    cancelled_reservations: int
    total_revenue: Decimal
    average_duration: float
    most_used_lot: Optional[str] = None

class ReservationDashboard(BaseSchema):
    """Schema for reservation dashboard data"""
    recent_reservations: List[ReservationResponse]
    stats: ReservationStats
    overdue_reservations: List[ReservationResponse]
    revenue_today: Decimal
    revenue_this_month: Decimal
