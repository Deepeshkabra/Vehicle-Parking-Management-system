"""
Admin routes for Vehicle Parking Management System
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError

# Import admin credentials from config
from config import Config

# Import models and utilities
from models import db, User, ParkingLot
from schemas.user import UserLogin, UserCreate, UserResponse
from schemas.parking_lot import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
    ParkingLotList,
    ParkingLotSummary,
    ParkingLotDelete,
)
from utils.error_handlers import (
    create_success_response,
    create_error_response,
    validate_request_data,
)
from utils.validation_utils import validate_user_permissions
from utils.cache_manager import cached_response, cached_query, cache_manager



admin_bp = Blueprint("admin", __name__)


blacklisted_tokens = set()


@admin_bp.route("/api/admin/users", methods=["GET"])
@jwt_required()
@cached_response("user_list", "user_list", 900)
def get_all_users():
    """Get All user details for admin"""
    jwt_data = get_jwt()
    # Check if user is admin
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        # Get all users
        users = User.query.all()
        return create_success_response("All users", [user.to_dict() for user in users])

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error retrieving users: {str(e)}")
        return jsonify({"error": "Database error occurred while retrieving users"}), 500
    except Exception as e:
        current_app.logger.error(f"Error getting users: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@admin_bp.route("/api/admin/pkl/create", methods=["POST"])
@jwt_required()
def create_pkl():
    """Create a new parking lot"""
    jwt_data = get_jwt()
    print(jwt_data)
    # Check if user is admin
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        data = request.get_json()
        print(data)
        parking_lot = ParkingLotCreate(
            prime_location_name=data["prime_location_name"],
            address=data["address"],
            pin_code=data["pin_code"],
            number_of_spots=data["number_of_spots"],
            price=data["price"],
        )
        # Fix: Use .dict() to unpack the validated data as keyword arguments
        new_parking_lot = ParkingLot(**parking_lot.model_dump())
        db.session.add(new_parking_lot)
        db.session.commit()

        new_parking_lot.create_parking_spots()
        db.session.commit()

        return create_success_response(
            "Parking lot created successfully", new_parking_lot.to_dict()
        )
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error creating parking lot: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error creating parking lot: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

@admin_bp.route("/api/admin/pkl/update/<int:lot_id>", methods=["POST"])
@jwt_required()
def update_pkl(lot_id):
    """Update a parking lot"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        data = request.get_json()
        parking_lot = ParkingLot.query.get_or_404(lot_id)
        parking_lot.prime_location_name = data.get("prime_location_name", parking_lot.prime_location_name)
        parking_lot.address = data.get("address", parking_lot.address)
        parking_lot.pin_code = data.get("pin_code", parking_lot.pin_code)
        parking_lot.number_of_spots = data.get("number_of_spots", parking_lot.number_of_spots)
        parking_lot.price = data.get("price", parking_lot.price)
        parking_lot.description = data.get("description", parking_lot.description)
        parking_lot.operating_hours_start = data.get("operating_hours_start", parking_lot.operating_hours_start)
        parking_lot.operating_hours_end = data.get("operating_hours_end", parking_lot.operating_hours_end)
        parking_lot.is_active = data.get("is_active", parking_lot.is_active)

        db.session.commit()
        return create_success_response("Parking lot updated successfully", parking_lot.to_dict())
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error updating parking lot: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error updating parking lot: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

@admin_bp.route("/api/admin/pkl/delete/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_pkl(lot_id):
    """Delete a parking lot"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        parking_lot = ParkingLot.query.get_or_404(lot_id)

        if parking_lot.is_empty():
            db.session.delete(parking_lot)
            db.session.commit()
            return create_success_response("Parking lot deleted successfully", parking_lot.to_dict())
        else:
            return create_error_response("Parking lot is not empty", status_code=400)
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error deleting parking lot: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error deleting parking lot: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

@admin_bp.route("/api/admin/pkl/<int:lot_id>", methods=["GET"])
@jwt_required()
@cached_response("parking_lots", "parking_lots_cache", 600)
def get_pkl(lot_id):
    """Get a parking lot"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        parking_lot = ParkingLot.query.get_or_404(lot_id)
        return create_success_response("Parking lot retrieved successfully", parking_lot.to_dict())
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error retrieving parking lot: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error retrieving parking lot: {str(e)}")

@admin_bp.route("/api/admin/pkl/list", methods=["GET"])
@jwt_required()
@cached_response("parking_lots", "parking_lots_cache", 600)
def get_all_pkl():
    """Get all parking lots"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        parking_lots = ParkingLot.query.all()
        return create_success_response("All parking lots", [pkl.to_dict() for pkl in parking_lots])
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error retrieving parking lots: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error retrieving parking lots: {str(e)}")
        return create_error_response("Internal server error", status_code=500)




