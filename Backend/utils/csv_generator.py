import csv
import os
import io
from datetime import datetime
from flask import current_app
from models.reservation import Reservation
from models.user import User
from models.parking_lot import ParkingLot

def generate_parking_csv(user_id, output_format='file', filename=None):
    """
    Generate CSV export of user's parking history
    
    Args:
        user_id (int): User ID to export data for
        output_format (str): 'file' or 'string' - format of output
        filename (str): Optional filename, auto-generated if None
    
    Returns:
        str: File path if output_format='file', CSV string if output_format='string'
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get all reservations for user
        reservations = Reservation.query.filter_by(user_id=user_id)\
            .order_by(Reservation.parking_timestamp.desc()).all()
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"parking_history_{user.username}_{timestamp}.csv"
        
        # Prepare CSV data
        csv_data = _prepare_reservation_csv_data(reservations)
        
        if output_format == 'file':
            # Write to file
            export_folder = current_app.config.get('EXPORT_FOLDER', './exports')
            os.makedirs(export_folder, exist_ok=True)
            filepath = os.path.join(export_folder, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                _write_csv_data(csvfile, csv_data)
            
            return filepath
        
        elif output_format == 'string':
            # Return as string
            output = io.StringIO()
            _write_csv_data(output, csv_data)
            csv_string = output.getvalue()
            output.close()
            return csv_string
        
        else:
            raise ValueError("output_format must be 'file' or 'string'")
    
    except Exception as e:
        current_app.logger.error(f"Error generating parking CSV for user {user_id}: {str(e)}")
        raise

def _prepare_reservation_csv_data(reservations):
    """Prepare reservation data for CSV export"""
    data = []
    
    for reservation in reservations:
        # Calculate duration
        duration_hours = None
        if reservation.parking_timestamp and reservation.leaving_timestamp:
            duration_seconds = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds()
            duration_hours = round(duration_seconds / 3600, 2)
        
        # Format timestamps
        parking_time = reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else ''
        leaving_time = reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else 'Still Parked'
        
        # Get parking lot info
        parking_lot = reservation.parking_spot.parking_lot if reservation.parking_spot else None
        lot_name = parking_lot.prime_location_name if parking_lot else 'Unknown'
        lot_address = parking_lot.address if parking_lot else 'Unknown'
        
        row = {
            'reservation_id': reservation.id,
            'slot_id': reservation.parking_spot.id if reservation.parking_spot else 'N/A',
            'spot_id': f"SPOT-{reservation.parking_spot.id}" if reservation.parking_spot else 'N/A',
            'parking_lot_name': lot_name,
            'parking_lot_address': lot_address,
            'parking_timestamp': parking_time,
            'leaving_timestamp': leaving_time,
            'duration_hours': duration_hours if duration_hours else 'N/A',
            'parking_cost': f"{reservation.parking_cost:.2f}" if reservation.parking_cost else '0.00',
            'currency': 'USD',
            'status': 'Completed' if reservation.leaving_timestamp else 'Active',
            'remarks': getattr(reservation, 'remarks', '') or '',
            'created_at': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(reservation, 'created_at') and reservation.created_at else ''
        }
        data.append(row)
    
    return data

def _write_csv_data(file_obj, data):
    """Write CSV data to file object"""
    if not data:
        # Write empty CSV with headers
        fieldnames = [
            'reservation_id', 'slot_id', 'spot_id', 'parking_lot_name', 'parking_lot_address',
            'parking_timestamp', 'leaving_timestamp', 'duration_hours', 'parking_cost',
            'currency', 'status', 'remarks', 'created_at'
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        return
    
    # Write data
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

def generate_admin_parking_lots_csv(filename=None):
    """
    Generate CSV export of all parking lots (Admin use)
    
    Args:
        filename (str): Optional filename
    
    Returns:
        str: File path to generated CSV
    """
    try:
        # Get all parking lots
        parking_lots = ParkingLot.query.all()
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"parking_lots_export_{timestamp}.csv"
        
        # Prepare data
        csv_data = []
        for lot in parking_lots:
            # Count available and occupied spots
            total_spots = len(lot.parking_spots) if lot.parking_spots else 0
            occupied_spots = len([spot for spot in lot.parking_spots if spot.status == 'O']) if lot.parking_spots else 0
            available_spots = total_spots - occupied_spots
            
            # Calculate total revenue for this lot
            total_revenue = 0
            if lot.parking_spots:
                for spot in lot.parking_spots:
                    spot_reservations = Reservation.query.filter_by(spot_id=spot.id).all()
                    total_revenue += sum(r.parking_cost for r in spot_reservations if r.parking_cost)
            
            row = {
                'lot_id': lot.id,
                'location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': f"{lot.price:.2f}" if hasattr(lot, 'price') and lot.price else '0.00',
                'total_spots': total_spots,
                'available_spots': available_spots,
                'occupied_spots': occupied_spots,
                'occupancy_rate': f"{(occupied_spots/total_spots*100):.1f}%" if total_spots > 0 else '0.0%',
                'total_revenue': f"{total_revenue:.2f}",
                'created_at': lot.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(lot, 'created_at') and lot.created_at else ''
            }
            csv_data.append(row)
        
        # Write to file
        export_folder = current_app.config.get('EXPORT_FOLDER', './exports')
        os.makedirs(export_folder, exist_ok=True)
        filepath = os.path.join(export_folder, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if csv_data:
                fieldnames = list(csv_data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            else:
                # Empty file with headers
                fieldnames = ['lot_id', 'location_name', 'address', 'pin_code', 'price_per_hour', 
                            'total_spots', 'available_spots', 'occupied_spots', 'occupancy_rate', 
                            'total_revenue', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        
        return filepath
    
    except Exception as e:
        current_app.logger.error(f"Error generating parking lots CSV: {str(e)}")
        raise

def generate_reservations_summary_csv(start_date=None, end_date=None, filename=None):
    """
    Generate CSV summary of all reservations within date range (Admin use)
    
    Args:
        start_date (datetime): Start date filter
        end_date (datetime): End date filter
        filename (str): Optional filename
    
    Returns:
        str: File path to generated CSV
    """
    try:
        # Build query
        query = Reservation.query
        
        if start_date:
            query = query.filter(Reservation.parking_timestamp >= start_date)
        if end_date:
            query = query.filter(Reservation.parking_timestamp <= end_date)
        
        reservations = query.order_by(Reservation.parking_timestamp.desc()).all()
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            date_suffix = ""
            if start_date and end_date:
                date_suffix = f"_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}"
            filename = f"reservations_summary{date_suffix}_{timestamp}.csv"
        
        # Prepare data
        csv_data = []
        for reservation in reservations:
            user = reservation.user if hasattr(reservation, 'user') else User.query.get(reservation.user_id)
            parking_spot = reservation.parking_spot
            parking_lot = parking_spot.parking_lot if parking_spot else None
            
            # Calculate duration
            duration_hours = None
            if reservation.parking_timestamp and reservation.leaving_timestamp:
                duration_seconds = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds()
                duration_hours = round(duration_seconds / 3600, 2)
            
            row = {
                'reservation_id': reservation.id,
                'user_id': reservation.user_id,
                'username': user.username if user else 'Unknown',
                'user_email': user.email if user else 'Unknown',
                'parking_lot_name': parking_lot.prime_location_name if parking_lot else 'Unknown',
                'spot_id': parking_spot.id if parking_spot else 'N/A',
                'parking_timestamp': reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else '',
                'leaving_timestamp': reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else 'Active',
                'duration_hours': duration_hours if duration_hours else 'N/A',
                'parking_cost': f"{reservation.parking_cost:.2f}" if reservation.parking_cost else '0.00',
                'status': 'Completed' if reservation.leaving_timestamp else 'Active',
                'created_at': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(reservation, 'created_at') and reservation.created_at else ''
            }
            csv_data.append(row)
        
        # Write to file
        export_folder = current_app.config.get('EXPORT_FOLDER', './exports')
        os.makedirs(export_folder, exist_ok=True)
        filepath = os.path.join(export_folder, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if csv_data:
                fieldnames = list(csv_data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            else:
                # Empty file with headers
                fieldnames = ['reservation_id', 'user_id', 'username', 'user_email', 
                            'parking_lot_name', 'spot_id', 'parking_timestamp', 
                            'leaving_timestamp', 'duration_hours', 'parking_cost', 
                            'status', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        
        return filepath
    
    except Exception as e:
        current_app.logger.error(f"Error generating reservations summary CSV: {str(e)}")
        raise

def generate_user_activity_csv(user_id, start_date=None, end_date=None):
    """
    Generate CSV of specific user's activity within date range
    
    Args:
        user_id (int): User ID
        start_date (datetime): Start date filter
        end_date (datetime): End date filter
    
    Returns:
        str: CSV content as string
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Build query
        query = Reservation.query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(Reservation.parking_timestamp >= start_date)
        if end_date:
            query = query.filter(Reservation.parking_timestamp <= end_date)
        
        reservations = query.order_by(Reservation.parking_timestamp.desc()).all()
        
        # Use existing function to generate CSV data
        return generate_parking_csv(user_id, output_format='string')
    
    except Exception as e:
        current_app.logger.error(f"Error generating user activity CSV for user {user_id}: {str(e)}")
        raise