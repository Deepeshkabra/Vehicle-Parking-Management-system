"""
User routes for Vehicle Parking Management System
"""

from flask import Blueprint, request, jsonify, current_app, send_file
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
    create_success_response,
    create_error_response,
    validate_request_data,
)
from utils.validation_utils import validate_user_permissions
from utils.cache_manager import cached_response, cached_query, cache_manager
from celery.result import AsyncResult
import os


user_bp = Blueprint("user", __name__)


@user_bp.route("/api/user/profile", methods=["GET"])
@jwt_required(locations=["headers"])
@cached_response("user_profile", "user_profile", 1800)
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
@cached_response("parking_lots", "parking_lots_cache", 600)
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
        available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
        if not available_spot:
            return create_error_response("No available spots", status_code=400)
        # Create reservation
        reservation = Reservation(
            user_id=user_id,
            spot_id=available_spot.id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now(),
            status="active",
            remarks="Reservation created successfully",
            hourly_rate=parking_lot.price,
        )
        db.session.add(reservation)
        available_spot.mark_occupied()
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

@user_bp.route("/api/user/export-csv", methods=["POST"])
@jwt_required()
def trigger_csv_export():
    """Trigger CSV export"""
    try:
        user_id = get_jwt_identity()
        email = request.json.get("email")

        celery = current_app.extensions['celery']


        task = celery.send_task('jobs.user_jobs.export_user_parking_csv', args=[user_id, email])

        return create_success_response("'Export started. You will receive an email with the CSV file shortly.", {"task_id": task.id})
    except Exception as e:
        current_app.logger.error(f"Error triggering CSV export: {str(e)}")
        return create_error_response("Internal server error", status_code=500)
    
@user_bp.route("/api/user/export-status/<string:task_id>", methods=["GET"])
def get_export_status(task_id):
    """Get the status of a CSV export task"""
    try:

        task = AsyncResult(task_id)
        if task.state == "PENDING":
            return create_success_response("Export is in progress", {"status": task.state})
        elif task.state == "PROGRESS":
            response = {
                "state": task.state,
                "current": task.info.get("current", 0),
                "total": task.info.get("total", 1),
                "status": task.info.get("status", ""),
            }
            return create_success_response("Export in progress", response)
        elif task.state == "SUCCESS":
            response = {
                "state": task.state,
                "result": task.result,
            }
            return create_success_response("Export completed", response)
        else:
            response = {
                "state": task.state,
                "error": str(task.info),
            }
            return create_error_response("Export failed", response)
    except Exception as e:
        current_app.logger.error(f"Error getting export status: {str(e)}")
        return create_error_response("Internal server error", status_code=500)

@user_bp.route("/api/user/download-csv/<filename>", methods=["GET"])
def download_csv(filename):
    """Download the CSV file"""
    try:
        file_path = os.path.join(current_app.config["EXPORT_FOLDER"], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return create_error_response("File not found", status_code=404)
    except Exception as e:
        current_app.logger.error(f"Error downloading CSV file: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


