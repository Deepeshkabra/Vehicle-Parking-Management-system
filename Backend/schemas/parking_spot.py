"""
Parking spot validation schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum
from .base import BaseSchema, TimestampMixin

class SpotStatus(str, Enum):
    """Parking spot status enumeration"""
    AVAILABLE = 'A'
    OCCUPIED = 'O'

class SpotType(str, Enum):
    """Parking spot type enumeration"""
    REGULAR = 'regular'
    HANDICAPPED = 'handicapped'
    VIP = 'vip'

class VehicleType(str, Enum):
    """Vehicle type enumeration"""
    FOUR_WHEELER = '4wheeler'

class ParkingSpotBase(BaseSchema):
    """Base parking spot schema"""
    lot_id: int = Field(..., gt=0, description="Parking lot ID")
    spot_number: int = Field(..., gt=0, description="Spot number")
    status: SpotStatus = Field(SpotStatus.AVAILABLE, description="Spot status")
    spot_type: SpotType = Field(SpotType.REGULAR, description="Spot type")
    vehicle_type: VehicleType = Field(VehicleType.FOUR_WHEELER, description="Vehicle type")

class ParkingSpotCreate(ParkingSpotBase):
    """Schema for creating parking spots"""
    
    class Config:
        schema_extra = {
            "example": {
                "lot_id": 1,
                "spot_number": 1,
                "status": "A",
                "spot_type": "regular",
                "vehicle_type": "4wheeler"
            }
        }

class ParkingSpotUpdate(BaseSchema):
    """Schema for updating parking spots"""
    status: Optional[SpotStatus] = Field(None, description="Spot status")
    spot_type: Optional[SpotType] = Field(None, description="Spot type")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "O",
                "spot_type": "regular"
            }
        }

class ParkingSpotResponse(ParkingSpotBase, TimestampMixin):
    """Schema for parking spot API responses"""
    id: int
    spot_identifier: str = Field(..., description="Unique spot identifier")
    is_available: bool = Field(..., description="Availability status")
    is_occupied: bool = Field(..., description="Occupancy status")
    current_reservation: Optional[dict] = Field(None, description="Current reservation details")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "lot_id": 1,
                "spot_number": 1,
                "status": "A",
                "spot_type": "regular",
                "vehicle_type": "4wheeler",
                "spot_identifier": "Downtown Central Plaza-1",
                "is_available": True,
                "is_occupied": False,
                "current_reservation": None,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }

class ParkingSpotList(BaseSchema):
    """Schema for parking spot list responses"""
    parking_spots: List[ParkingSpotResponse]
    total: int
    page: int
    per_page: int

class ParkingSpotFilter(BaseSchema):
    """Schema for parking spot filtering"""
    lot_id: Optional[int] = Field(None, gt=0, description="Filter by parking lot")
    status: Optional[SpotStatus] = Field(None, description="Filter by status")
    spot_type: Optional[SpotType] = Field(None, description="Filter by spot type")
    available_only: Optional[bool] = Field(None, description="Show only available spots")

class ParkingSpotBulkUpdate(BaseSchema):
    """Schema for bulk updating parking spots"""
    spot_ids: List[int] = Field(..., min_items=1, description="List of spot IDs")
    status: Optional[SpotStatus] = Field(None, description="New status")
    spot_type: Optional[SpotType] = Field(None, description="New spot type")
    
    @field_validator('spot_ids')
    def validate_spot_ids(cls, v):
        if len(v) > 100:
            raise ValueError('Cannot update more than 100 spots at once')
        if len(set(v)) != len(v):
            raise ValueError('Duplicate spot IDs are not allowed')
        return v
