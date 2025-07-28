"""
Validation utility functions
"""

from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from flask import jsonify
import re
from datetime import datetime, time


def validate_business_hours(start_time: time, end_time: time) -> bool:
    """Validate business hours"""
    if start_time >= end_time:
        return False
    return True


def validate_reservation_time_slot(
    parking_timestamp: datetime, leaving_timestamp: Optional[datetime] = None
) -> bool:
    """Validate reservation time slot"""
    if leaving_timestamp and leaving_timestamp <= parking_timestamp:
        return False
    return True


def validate_spot_availability(spot_status: str, reservation_status: str) -> bool:
    """Validate spot availability for reservation"""
    if spot_status == "O" and reservation_status == "active":
        return False
    return True


def validate_user_permissions(user_role: str, required_role: str) -> bool:
    """Validate user permissions"""
    role_hierarchy = {"user": 0, "admin": 1}
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)


def validate_lot_deletion(occupied_spots: int) -> bool:
    """Validate if parking lot can be deleted"""
    return occupied_spots == 0


def validate_spot_number_uniqueness(
    lot_id: int, spot_number: int, existing_spots: List[Dict]
) -> bool:
    """Validate spot number uniqueness within a lot"""
    for spot in existing_spots:
        if spot["lot_id"] == lot_id and spot["spot_number"] == spot_number:
            return False
    return True


def validate_email_domain(
    email: str, allowed_domains: Optional[List[str]] = None
) -> bool:
    """Validate email domain"""
    if not allowed_domains:
        return True

    domain = email.split("@")[1].lower()
    return domain in [d.lower() for d in allowed_domains]


def validate_indian_pin_code(pin_code: str) -> bool:
    """Validate Indian PIN code format"""
    return bool(re.match(r"^[1-9][0-9]{5}$", pin_code))


def validate_time_format(time_str: str) -> bool:
    """Validate time format HH:MM"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def validate_date_range(
    start_date: datetime, end_date: datetime, max_days: int = 365
) -> bool:
    """Validate date range"""
    if end_date <= start_date:
        return False

    if (end_date - start_date).days > max_days:
        return False

    return True


def validate_decimal_precision(value: float, max_decimal_places: int = 2) -> bool:
    """Validate decimal precision"""
    decimal_places = len(str(value).split(".")[1]) if "." in str(value) else 0
    return decimal_places <= max_decimal_places


def sanitize_text_input(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return text

    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', "", text)

    # Trim whitespace
    sanitized = sanitized.strip()

    return sanitized


def validate_file_size(file_size: int, max_size_mb: int = 5) -> bool:
    """Validate file size"""
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes


def validate_image_format(filename: str) -> bool:
    """Validate image file format"""
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    file_extension = filename.lower().split(".")[-1]
    return f".{file_extension}" in allowed_extensions


def validate_csv_headers(headers: List[str], required_headers: List[str]) -> bool:
    """Validate CSV headers"""
    return all(header in headers for header in required_headers)


def format_validation_error(error: ValidationError) -> Dict[str, Any]:
    """Format Pydantic validation error for API response"""
    formatted_errors = []
    field_errors = {}

    for err in error.errors():
        field_path = " -> ".join(str(x) for x in err["loc"])
        error_message = err["msg"]
        error_type = err["type"]

        formatted_errors.append(
            {"field": field_path, "message": error_message, "type": error_type}
        )

        if field_path not in field_errors:
            field_errors[field_path] = []
        field_errors[field_path].append(error_message)

    return {
        "error": "Validation failed",
        "details": formatted_errors,
        "field_errors": field_errors,
    }


def validate_pagination_params(
    page: int, per_page: int, max_per_page: int = 100
) -> bool:
    """Validate pagination parameters"""
    return page >= 1 and 1 <= per_page <= max_per_page


def validate_sort_params(sort_by: str, allowed_fields: List[str]) -> bool:
    """Validate sort parameters"""
    return sort_by in allowed_fields


def validate_phone_number_format(phone: str) -> bool:
    """Validate phone number format"""
    # Remove common separators
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)

    # Check for valid international format
    return bool(re.match(r"^\+?[\d]{10,15}$", cleaned))


def validate_vehicle_number_format(vehicle_number: str) -> bool:
    """Validate vehicle number format"""
    # Indian vehicle number format: XX00XX0000 or XX-00-XX-0000
    patterns = [
        r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$",  # XX00XX0000
        r"^[A-Z]{2}-[0-9]{2}-[A-Z]{2}-[0-9]{4}$",  # XX-00-XX-0000
        r"^[A-Z]{2}[0-9]{2}[A-Z]{1}[0-9]{4}$",  # XX00X0000
        r"^[A-Z]{2}-[0-9]{2}-[A-Z]{1}-[0-9]{4}$",  # XX-00-X-0000
    ]

    return any(re.match(pattern, vehicle_number.upper()) for pattern in patterns)
