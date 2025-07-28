"""
Parking lot validation schemas
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import time
from decimal import Decimal
from .base import BaseSchema, TimestampMixin, validate_pin_code


class ParkingLotBase(BaseSchema):
    """Base parking lot schema"""

    prime_location_name: str = Field(
        ..., min_length=3, max_length=100, description="Location name"
    )
    address: str = Field(..., min_length=10, description="Full address")
    pin_code: str = Field(..., description="PIN code")
    number_of_spots: int = Field(
        ..., ge=1, le=1000, description="Number of parking spots"
    )
    price: Decimal = Field(..., ge=0, le=10000, description="Price per hour")
    description: Optional[str] = Field(None, max_length=1000, description="Description")
    operating_hours_start: Optional[time] = Field(None, description="Opening time")
    operating_hours_end: Optional[time] = Field(None, description="Closing time")

    @field_validator("prime_location_name")
    def validate_location_name(cls, v):
        # Allow letters, numbers, spaces, hyphens, and basic punctuation
        import re

        if not re.match(r"^[a-zA-Z0-9\s\-\.,\']+$", v):
            raise ValueError("Location name contains invalid characters")
        return v.strip()

    @field_validator("pin_code")
    def validate_pin_code_format(cls, v):
        return validate_pin_code(v)

    @field_validator("address")
    def validate_address(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Address must be at least 10 characters long")
        return v.strip()

    @field_validator("price")
    def validate_price_precision(cls, v):
        # Ensure price has at most 2 decimal places
        if v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        return v

    @field_validator("operating_hours_end")
    def validate_operating_hours(cls, v, values):
        if v is not None and "operating_hours_start" in values:
            start_time = values["operating_hours_start"]
            if start_time is not None and v <= start_time:
                raise ValueError("Closing time must be after opening time")
        return v


class ParkingLotCreate(ParkingLotBase):
    """Schema for creating parking lots"""

    is_active: Optional[bool] = Field(True, description="Active status")

    class Config:
        schema_extra = {
            "example": {
                "prime_location_name": "Downtown Central Plaza",
                "address": "123 Main Street, Downtown District, City",
                "pin_code": "123456",
                "number_of_spots": 50,
                "price": 25.00,
                "description": "Prime downtown location with 24/7 security",
                "operating_hours_start": "06:00",
                "operating_hours_end": "22:00",
                "is_active": True,
            }
        }


class ParkingLotUpdate(BaseSchema):
    """Schema for updating parking lots"""

    prime_location_name: Optional[str] = Field(None, min_length=3, max_length=100)
    address: Optional[str] = Field(None, min_length=10)
    pin_code: Optional[str] = Field(None)
    number_of_spots: Optional[int] = Field(None, ge=1, le=1000)
    price: Optional[Decimal] = Field(None, ge=0, le=10000)
    description: Optional[str] = Field(None, max_length=1000)
    operating_hours_start: Optional[time] = Field(None)
    operating_hours_end: Optional[time] = Field(None)
    is_active: Optional[bool] = Field(None)

    @field_validator("prime_location_name")
    def validate_location_name(cls, v):
        if v is not None:
            import re

            if not re.match(r"^[a-zA-Z0-9\s\-\.,\']+$", v):
                raise ValueError("Location name contains invalid characters")
            return v.strip()
        return v

    @field_validator("pin_code")
    def validate_pin_code_format(cls, v):
        if v is not None:
            return validate_pin_code(v)
        return v

    @field_validator("address")
    def validate_address(cls, v):
        if v is not None and len(v.strip()) < 10:
            raise ValueError("Address must be at least 10 characters long")
        return v.strip() if v else v

    @field_validator("price")
    def validate_price_precision(cls, v):
        if v is not None and v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        return v

    @field_validator("operating_hours_end")
    def validate_operating_hours(cls, v, values):
        if v is not None and "operating_hours_start" in values:
            start_time = values["operating_hours_start"]
            if start_time is not None and v <= start_time:
                raise ValueError("Closing time must be after opening time")
        return v


class ParkingLotResponse(ParkingLotBase, TimestampMixin):
    """Schema for parking lot API responses"""

    id: int
    is_active: bool
    available_spots: int = Field(..., description="Available parking spots")
    occupied_spots: int = Field(..., description="Occupied parking spots")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "prime_location_name": "Downtown Central Plaza",
                "address": "123 Main Street, Downtown District, City",
                "pin_code": "123456",
                "number_of_spots": 50,
                "price": 25.00,
                "description": "Prime downtown location with 24/7 security",
                "operating_hours_start": "06:00",
                "operating_hours_end": "22:00",
                "is_active": True,
                "available_spots": 35,
                "occupied_spots": 15,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }


class ParkingLotList(BaseSchema):
    """Schema for parking lot list responses"""

    parking_lots: List[ParkingLotResponse]
    total: int
    page: int
    per_page: int


class ParkingLotSummary(BaseSchema):
    """Schema for parking lot summary"""

    id: int
    prime_location_name: str
    available_spots: int
    total_spots: int
    price: Decimal
    is_active: bool


class ParkingLotDelete(BaseSchema):
    """Schema for parking lot deletion validation"""

    confirm_deletion: bool = Field(..., description="Confirm deletion")

    @field_validator("confirm_deletion")
    def validate_confirmation(cls, v):
        if not v:
            raise ValueError("Deletion must be confirmed")
        return v
