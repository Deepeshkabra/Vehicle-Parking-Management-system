"""
User routes for Vehicle Parking Management System
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
from models import db, User, ParkingLot, Reservation, ParkingSpot
from schemas.user import UserResponse
from schemas.parking_lot import (
    ParkingLotResponse,
    ParkingLotList,

)
from utils.error_handlers import (
    ValidationException,
    UnauthorizedException,
    ForbiddenException,
    create_success_response,
    create_error_response,
    validate_request_data,
)
from utils.validation_utils import validate_user_permissions

user_bp = Blueprint("user", __name__)


@user_bp.route("/api/user/profile", methods=["GET"])
@jwt_required(locations=["headers"])
def get_user_profile():
    """Get user profile"""
    jwt_data = get_jwt()
    print(jwt_data)
    if jwt_data.get("role") != "user":
        return create_error_response("Unauthorized access", status_code=403)
    try:
        user_id = jwt_data.get("sub")
        user = User.query.get_or_404(user_id)
        return create_success_response("User profile retrieved successfully", user.to_dict())
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error retrieving user profile: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error retrieving user profile: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

@user_bp.route("/api/user/profile/update", methods=["POST"])
@jwt_required()
def update_user_profile():
    """Update user profile"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "user":
        return create_error_response("Unauthorized access", status_code=403)
    try:
        data = request.get_json()
        user_id = jwt_data.get("sub")
        user = User.query.get_or_404(user_id)
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        db.session.commit()

        return create_success_response("User profile updated successfully", user.to_dict())
    
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error updating user profile: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error updating user profile: {str(e)}")
        return create_error_response("Internal server error", status_code=500)
    
@user_bp.route("/api/user/pkl/list", methods=["GET"])
@jwt_required()
def get_all_pkl():
    """Get all parking lots for user"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "user":
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
    
@user_bp.route("/api/user/pkl/book/<int:lot_id>", methods=["POST"])
@jwt_required()
def book_pkl(lot_id):
    """Book a parking lot"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "user":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        vehicle_number = request.json.get("vehicle_number")
        user_id = jwt_data.get("sub")
        parking_lot = ParkingLot.query.get_or_404(lot_id)
        spot_id = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first().id      
        
        if not spot_id:
            return create_error_response("No available spots", status_code=400)
        # Create reservation
        reservation = Reservation(
            user_id=user_id,
            spot_id=spot_id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now(),
            status="active",
            remarks="Reservation created successfully",
            hourly_rate=parking_lot.price,
        )
        db.session.add(reservation)
        db.session.commit()
        return create_success_response("Reservation created successfully", reservation.to_dict())
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error creating reservation: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error creating reservation: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@user_bp.route("/api/user/pkl/release", methods=["POST"])
@jwt_required()
def release_reservation():
    "Getting the release TimeStamp and cost of reservation for users for entire parking duration"
    jwt_data = get_jwt()
    if jwt_data.get("role") != "user":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        user_id = jwt_data.get("sub")
        reservation = Reservation.query.filter_by(user_id=user_id, status="active").first()
        if not reservation:
            return create_error_response("No active reservation", status_code=400)
        reservation.complete_reservation()
        db.session.commit()
        return create_success_response("Reservation completed successfully", reservation.to_dict())
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error completing reservation: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error completing reservation: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@user_bp.route("/api/user/pkl/book/list", methods=["GET"])
@jwt_required()
def get_all_bookings():
    """Get all bookings for user"""
    jwt_data = get_jwt()
    if jwt_data.get("role") != "user":
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        user_id = jwt_data.get("sub")
        print(user_id)
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        return create_success_response("All bookings", [reservation.to_dict() for reservation in reservations])
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error retrieving bookings: {str(e)}")
        return create_error_response("Database error", status_code=500)
    except Exception as e:
        current_app.logger.error(f"Error retrieving bookings: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

