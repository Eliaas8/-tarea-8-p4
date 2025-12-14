from flask_mail import Message
from celery import shared_task
from app import mail
import os

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def send_email_task(self, action, title):
    msg = Message(
        subject=f'Biblioteca - {action}',
        sender=os.getenv('MAIL_USERNAME'),
        recipients=[os.getenv('MAIL_USERNAME')],
        body=f'El libro "{title}" fue procesado correctamente.'
    )
    mail.send(msg)
