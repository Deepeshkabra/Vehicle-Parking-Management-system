"""
Flask application for Vehicle Parking Management System
This module sets up the Flask app with JWT authentication, database models, and routes
"""

import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jobs import user_jobs
from flask_mail import Mail
# Import configuration
from config import Config, DevelopmentConfig

# Import CORS
from flask_cors import CORS

# Import models to register them with SQLAlchemy
from models import db, User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation

# Import routes
from routes.auth import auth_bp, check_if_token_revoked
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp


from jobs.celery_app import make_celery, configure_celery

from utils.cache_manager import CacheManager

# Import error handlers
from utils.error_handlers import register_error_handlers


def create_app(config_class=DevelopmentConfig):
    """
    Application factory pattern for creating Flask app

    Args:
        config_class: Configuration class to use

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    configure_celery(app)
    celery = make_celery(app)
    mail = Mail(app)

    #Initialize Cache
    cache_manager = CacheManager(app)
    
    app.extensions['celery'] = celery
    app.extensions['mail'] = mail
    with app.app_context():
        from jobs.celery_app import user_jobs
    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize CORS
    cors = CORS()
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Configure JWT settings
    jwt.token_in_blocklist_loader(check_if_token_revoked)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Token has expired",
                    "message": "The token has expired. Please login again.",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Authorization token required",
                    "message": "Authorization header with valid token is required.",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Token has been revoked",
                    "message": "The token has been revoked. Please login again.",
                }
            ),
            401,
        )

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    # Register error handlers
    register_error_handlers(app)

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Simple health check endpoint"""
        return jsonify(
            {
                "success": True,
                "message": "Vehicle Parking Management System API is running",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
            }
        )

    # Root endpoint
    @app.route("/")
    def home():
        """Root endpoint with API information"""
        return jsonify(
            {
                "message": "Vehicle Parking Management System API",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/api/health",
                    "auth": {
                        "register": "/api/auth/register",
                        "login": "/api/auth/login",
                        "refresh": "/api/auth/refresh",
                        "logout": "/api/auth/logout",
                        "me": "/api/auth/me",
                    },
                },
            }
        )

    return app, celery


# Create app instance
app, celery = create_app()

if __name__ == "__main__":
    app.run(debug=True)
