#!/usr/bin/env python3
"""
Database initialization script for Vehicle Parking App
Run this script to create the database and initialize with sample data
"""
import os
import sys
import argparse
from flask import Flask
from config import Config, DevelopmentConfig
from models import db, init_db
from models.db_utils import create_database, reset_database, get_database_stats, create_sample_data

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    return app

def main():
    """Main function to handle database initialization"""
    parser = argparse.ArgumentParser(description='Initialize Vehicle Parking App Database')
    parser.add_argument('--reset', action='store_true', help='Reset database (drop and recreate)')
    parser.add_argument('--no-sample', action='store_true', help='Skip creating sample data')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    # Create Flask app
    app = create_app()
    
    if args.stats:
        # Show database statistics
        stats = get_database_stats(app)
        print("\n=== Database Statistics ===")
        print(f"Total Users: {stats['total_users']}")
        print(f"  - Admin Users: {stats['admin_users']}")
        print(f"  - Regular Users: {stats['regular_users']}")
        print(f"Total Parking Lots: {stats['total_parking_lots']}")
        print(f"  - Active Parking Lots: {stats['active_parking_lots']}")
        print(f"Total Parking Spots: {stats['total_parking_spots']}")
        print(f"  - Available Spots: {stats['available_spots']}")
        print(f"  - Occupied Spots: {stats['occupied_spots']}")
        print(f"Total Reservations: {stats['total_reservations']}")
        print(f"  - Active Reservations: {stats['active_reservations']}")
        print(f"  - Completed Reservations: {stats['completed_reservations']}")
        print(f"  - Cancelled Reservations: {stats['cancelled_reservations']}")
        print("========================\n")
        return
    
    if args.reset:
        # Reset database
        print("Resetting database...")
        reset_database(app)
        if not args.no_sample:
            with app.app_context():
                create_sample_data()
        print("Database reset completed!")
        return
    
    # Check if database exists
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_exists = os.path.exists(db_path)
    
    if db_exists:
        print(f"Database already exists at: {db_path}")
        response = input("Do you want to recreate it? (y/N): ").lower()
        if response != 'y':
            print("Database initialization cancelled.")
            return
    
    # Create database
    print("Creating database...")
    with app.app_context():
        # Initialize database
        db.init_app(app)
        db.create_all()
        
        # Create sample data if requested
        if not args.no_sample:
            create_sample_data()
            print("Sample data created successfully!")
    
    print(f"Database created successfully at: {db_path}")
    
    if not args.no_sample:
        print("\nSample user credentials:")
        print("  Username: john_doe, Password: password123")
        print("  Username: jane_smith, Password: password123")
        print("  Username: mike_johnson, Password: password123")

if __name__ == '__main__':
    main() 