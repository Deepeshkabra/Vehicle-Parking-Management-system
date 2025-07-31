from celery import current_app as celery_app
from datetime import datetime, timedelta
from flask import current_app
from models.user import User
from models.parking_lot import ParkingLot
from models.reservation import Reservation
from utils.csv_generator import generate_parking_csv
from utils.notification import send_email
from utils.report_generator import generate_monthly_html_report

import logging

@celery_app.task
def send_daily_reminders():
    """
    Daily job to send reminders to users who haven't visited
    or when new parking lots are created
    """
    try:
        current_app.logger.info("Starting daily reminders job")
        
        # Get all active users
        users = User.query.filter_by(role='user', is_active=True).all()
        
        # Check for users who haven't made reservations in last 3 days
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        
        for user in users:
            last_reservation = Reservation.query.filter_by(user_id=user.id)\
                .order_by(Reservation.created_at.desc()).first()
            
            should_send_reminder = False
            message = ""
            
            # Check if user hasn't visited recently
            if not last_reservation or last_reservation.created_at < three_days_ago:
                should_send_reminder = True
                message = f"Hi {user.username}! 🚗 Haven't seen you in a while. Check out available parking spots and book if needed!"
            
            # Check for new parking lots created in last 24 hours
            yesterday = datetime.utcnow() - timedelta(days=1)
            new_lots = ParkingLot.query.filter(ParkingLot.created_at >= yesterday).all()
            
            if new_lots and not should_send_reminder:
                should_send_reminder = True
                lot_names = [lot.prime_location_name for lot in new_lots]
                message = f"Hi {user.username}! 🆕 New parking lots available: {', '.join(lot_names)}. Book your spot now!"
            
            if should_send_reminder:
                try:
                    send_email(
                        subject="Parking Reminder 🚗",
                        recipients=[user.email],
                        text_body=message,
                        html_body=f"<p>{message}</p>"
                    )
                    current_app.logger.info(f"Reminder sent to {user.email}")
                except Exception as e:
                    current_app.logger.error(f"Error sending reminder to {user.email}: {str(e)}")
        
        current_app.logger.info(f"Daily reminders sent to {len(users)} users")
        return f"Reminders processed for {len(users)} users"
        
    except Exception as e:
        current_app.logger.error(f"Error in daily reminders: {str(e)}")
        raise


@celery_app.task
def generate_monthly_report():
    """
    Generate and send monthly activity reports to all users
    """
    try:
        current_app.logger.info("Starting monthly report generation")
        
        # Get all users
        users = User.query.filter_by(role='user', is_active=True).all()
        
        # Get date range for last month
        today = datetime.now()
        first_day_last_month = datetime(today.year, today.month - 1, 1)
        last_day_last_month = datetime(today.year, today.month, 1) - timedelta(days=1)
        
        reports_sent = 0
        
        for user in users:
            try:
                # DIRECT FUNCTION CALL instead of .delay()
                start_dt = datetime(2025, 7, 1)
                end_dt = datetime(2025, 8, 1)
                
                # Get user's reservations for the month
                reservations = Reservation.query.filter(
                    Reservation.user_id == user.id,
                    Reservation.parking_timestamp >= start_dt,
                    Reservation.parking_timestamp <= end_dt
                ).all()
                
                if not reservations:
                    current_app.logger.info(f"No activity for user {user.username} in the specified period")
                    continue
                
                # Calculate statistics
                total_bookings = len(reservations)
                total_cost = sum(r.parking_cost for r in reservations if r.parking_cost)
                
                # Most used parking lot
                lot_usage = {}
                for reservation in reservations:
                    lot_name = reservation.parking_spot.parking_lot.prime_location_name
                    lot_usage[lot_name] = lot_usage.get(lot_name, 0) + 1
                
                most_used_lot = max(lot_usage.items(), key=lambda x: x[1]) if lot_usage else None
                
                # Generate HTML report
                report_data = {
                    'user': user,
                    'month_year': start_dt.strftime('%B %Y'),
                    'total_bookings': total_bookings,
                    'total_cost': total_cost,
                    'most_used_lot': most_used_lot,
                    'lot_usage': lot_usage,
                    'reservations': reservations
                }
                
                html_report = generate_monthly_html_report(report_data)
                
                # Send email with HTML report
                send_email(
                    subject=f"Monthly Parking Report - {start_dt.strftime('%B %Y')}",
                    recipients=[user.email],
                    text_body=f"Your monthly parking report for {start_dt.strftime('%B %Y')} is ready.",
                    html_body=html_report
                )
                
                reports_sent += 1
                current_app.logger.info(f"Monthly report sent to {user.email}")
                
            except Exception as user_error:
                current_app.logger.error(f"Error generating report for user {user.username}: {str(user_error)}")
                # Continue with other users even if one fails
        
        return f"Monthly reports sent to {reports_sent}/{len(users)} users"
        
    except Exception as e:
        current_app.logger.error(f"Error in monthly report generation: {str(e)}")
        raise


# Update the export_user_parking_csv function
@celery_app.task(bind=True)
def export_user_parking_csv(self, user_id, email):
    """
    Export user's complete parking history as CSV
    This is a user-triggered async job
    """
    try:
        # Update task state
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting export...'})
        
        user = User.query.get(user_id)
        if not user:
            raise Exception(f"User {user_id} not found")
        
        # Update progress
        self.update_state(state='PROGRESS', meta={'current': 30, 'total': 100, 'status': 'Generating CSV...'})
        
        # Generate CSV using utility function
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"parking_history_{user.username}_{timestamp}.csv"
        
        filepath = generate_parking_csv(user_id, output_format='file', filename=filename)
        
        # Update progress
        self.update_state(state='PROGRESS', meta={'current': 80, 'total': 100, 'status': 'Sending notification...'})
        
        download_url = f"{current_app.config['BACKEND_URL']}/api/user/download-csv/{filename}"
        
        # Send completion email
        send_email(
            subject="Parking History Export Ready 📊",
            recipients=[email],
            text_body=f"Your parking history export is ready for download.",
            html_body=f"""
            <h2>Your Parking History Export is Ready!</h2>
            <p>Hello {user.username},</p>
            <p>Your parking history export has been completed and is ready for download.</p>
            <p><a href="{download_url}" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Download CSV</a></p>
            <p>The file will be available for 7 days.</p>
            <p>Best regards,<br>Vehicle Parking Management System</p>
            """
        )
        
        self.update_state(state='SUCCESS', meta={'current': 100, 'total': 100, 'status': 'Export completed successfully'})
        
        return {
            'status': 'completed',
            'filename': filename,
            'download_url': download_url
        }
        
    except Exception as e:
        current_app.logger.error(f"CSV export failed for user {user_id}: {str(e)}")
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
