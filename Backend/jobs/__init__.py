from celery import current_app as celery_app
from flask import current_app
from models.user import User
from models.reservation import Reservation
from utils.notification import send_email
from utils.csv_generator import generate_parking_csv
import os
import csv
from datetime import datetime, timedelta

# @celery_app.task(bind=True)
# def export_user_parking_csv(self, user_id, email):
#     """
#     Export user's complete parking history as CSV
#     This is a user-triggered async job
#     """
#     try:
#         # Update task state
#         self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting export...'})
        
#         user = User.query.get(user_id)
#         if not user:
#             raise Exception(f"User {user_id} not found")
        
#         # Get all user reservations
#         self.update_state(state='PROGRESS', meta={'current': 20, 'total': 100, 'status': 'Fetching reservations...'})
        
#         reservations = Reservation.query.filter_by(user_id=user_id)\
#             .order_by(Reservation.parking_timestamp.desc()).all()
        
#         if not reservations:
#             self.update_state(state='PROGRESS', meta={'current': 100, 'total': 100, 'status': 'No reservations found'})
#             return {'status': 'completed', 'message': 'No parking history found for export'}
        
#         # Create CSV file
#         self.update_state(state='PROGRESS', meta={'current': 40, 'total': 100, 'status': 'Generating CSV...'})
        
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f"parking_history_{user.username}_{timestamp}.csv"
#         filepath = os.path.join(current_app.config['EXPORT_FOLDER'], filename)
        
#         # Ensure export directory exists
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
#         # Generate CSV
#         self.update_state(state='PROGRESS', meta={'current': 60, 'total': 100, 'status': 'Writing CSV data...'})
        
#         with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
#             fieldnames = [
#                 'reservation_id',
#                 'slot_id', 
#                 'spot_id',
#                 'parking_lot_name',
#                 'parking_timestamp',
#                 'leaving_timestamp',
#                 'duration_hours',
#                 'parking_cost',
#                 'status',
#                 'remarks'
#             ]
            
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
            
#             for i, reservation in enumerate(reservations):
#                 # Calculate duration
#                 duration = None
#                 if reservation.leaving_timestamp and reservation.parking_timestamp:
#                     duration = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
                
#                 writer.writerow({
#                     'reservation_id': reservation.id,
#                     'slot_id': reservation.parking_spot.id,
#                     'spot_id': f"SPOT-{reservation.parking_spot.id}",
#                     'parking_lot_name': reservation.parking_spot.parking_lot.prime_location_name,
#                     'parking_timestamp': reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else '',
#                     'leaving_timestamp': reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else 'Still Parked',
#                     'duration_hours': f"{duration:.2f}" if duration else 'N/A',
#                     'parking_cost': f"${reservation.parking_cost:.2f}" if reservation.parking_cost else '$0.00',
#                     'status': 'Completed' if reservation.leaving_timestamp else 'Active',
#                     'remarks': getattr(reservation, 'remarks', '') or ''
#                 })
                
#                 # Update progress
#                 progress = 60 + (i / len(reservations)) * 30
#                 self.update_state(state='PROGRESS', meta={'current': int(progress), 'total': 100, 'status': f'Processing record {i+1}/{len(reservations)}'})
        
#         # Send completion email with download link
#         self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100, 'status': 'Sending notification...'})
        
#         download_url = f"{current_app.config['BACKEND_URL']}/api/user/download-csv/{filename}"
        
#         send_email(
#             to=email,
#             subject="Parking History Export Ready 📊",
#             template="csv_export_complete.html",
#             user=user,
#             filename=filename,
#             download_url=download_url,
#             total_records=len(reservations)
#         )
        
#         # Send in-app notification (if you have notification system)
#         create_user_notification.delay(
#             user_id, 
#             "CSV Export Complete", 
#             f"Your parking history export ({len(reservations)} records) is ready for download.",
#             download_url
#         )
        
#         self.update_state(state='SUCCESS', meta={'current': 100, 'total': 100, 'status': 'Export completed successfully'})
        
#         return {
#             'status': 'completed',
#             'filename': filename,
#             'records_count': len(reservations),
#             'download_url': download_url
#         }
        
#     except Exception as e:
#         current_app.logger.error(f"CSV export failed for user {user_id}: {str(e)}")
#         self.update_state(state='FAILURE', meta={'error': str(e)})
#         raise

@celery_app.task
def create_user_notification(user_id, title, message, action_url=None):
    """Create in-app notification for user"""
    try:
        # Implement your notification system here
        # This could be stored in database, sent via websocket, etc.
        pass
    except Exception as e:
        current_app.logger.error(f"Failed to create notification for user {user_id}: {str(e)}")

@celery_app.task
def cleanup_old_csv_files():
    """Cleanup old CSV export files (run weekly)"""
    try:
        export_folder = current_app.config['EXPORT_FOLDER']
        cutoff_date = datetime.now() - timedelta(days=7)  # Delete files older than 7 days
        
        for filename in os.listdir(export_folder):
            filepath = os.path.join(export_folder, filename)
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_modified < cutoff_date:
                    os.remove(filepath)
                    current_app.logger.info(f"Deleted old export file: {filename}")
        
        return "CSV cleanup completed"
    except Exception as e:
        current_app.logger.error(f"CSV cleanup failed: {str(e)}")
        raise