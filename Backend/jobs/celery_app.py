from celery import Celery
from celery.schedules import crontab
from flask import Flask
from jobs import user_jobs
import os

def make_celery(app):
    """Factory function to create Celery instance with Flask app context"""
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Celery configuration
def configure_celery(app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERY_TIMEZONE'] = 'UTC'
    
    # Beat schedule for periodic tasks
    app.config['BEAT_SCHEDULE'] = {
        'daily-reminders': {
            'task': 'jobs.user_jobs.send_daily_reminders',
            'schedule': crontab(minute='*/2'),  # 6 PM daily
        },
        'monthly-report': {
            'task': 'jobs.user_jobs.generate_monthly_report',
            'schedule': crontab(minute='*/2'),  # 1st of month at 9 AM
        },
    }