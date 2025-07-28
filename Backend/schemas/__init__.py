"""
Schemas package initialization
"""

from .base import (
    BaseSchema,
    TimestampMixin,
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse,
)

from .user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserList,
    UserPasswordReset,
    UserPasswordResetConfirm,
)

from .parking_lot import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
    ParkingLotList,
    ParkingLotSummary,
    ParkingLotDelete,
)

from .parking_spot import (
    ParkingSpotCreate,
    ParkingSpotUpdate,
    ParkingSpotResponse,
    ParkingSpotList,
    ParkingSpotFilter,
    ParkingSpotBulkUpdate,
    SpotStatus,
    SpotType,
    VehicleType,
)

from .reservation import (
    ReservationCreate,
    ReservationUpdate,
    ReservationComplete,
    ReservationCancel,
    ReservationResponse,
    ReservationList,
    ReservationFilter,
    ReservationCSV,
    ReservationStats,
    ReservationDashboard,
    ReservationStatus,
)

# Export all schemas
__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampMixin",
    "PaginationParams",
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorResponse",
    # User schemas
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserList",
    "UserPasswordReset",
    "UserPasswordResetConfirm",
    # Parking lot schemas
    "ParkingLotCreate",
    "ParkingLotUpdate",
    "ParkingLotResponse",
    "ParkingLotList",
    "ParkingLotSummary",
    "ParkingLotDelete",
    # Parking spot schemas
    "ParkingSpotCreate",
    "ParkingSpotUpdate",
    "ParkingSpotResponse",
    "ParkingSpotList",
    "ParkingSpotFilter",
    "ParkingSpotBulkUpdate",
    "SpotStatus",
    "SpotType",
    "VehicleType",
    # Reservation schemas
    "ReservationCreate",
    "ReservationUpdate",
    "ReservationComplete",
    "ReservationCancel",
    "ReservationResponse",
    "ReservationList",
    "ReservationFilter",
    "ReservationCSV",
    "ReservationStats",
    "ReservationDashboard",
    "ReservationStatus",
]
