from flask_mail import Message
from flask import current_app


def send_email(subject, recipients, text_body, html_body):
    """Send an email using Flask-Mail."""
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    current_app.extensions['mail'].send(msg)

