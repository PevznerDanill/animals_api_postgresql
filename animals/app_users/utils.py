import traceback
from .models import User
from django.core import mail
from django.conf import settings
from .models import User
import smtplib, ssl


def send_email_to_upgrade(user: User):
    admin_mail = User.objects.only('email').get(is_superuser=True).email
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    subject = 'New request to upgrade user'
    message = f'The user {user.username} with id {user.id} asks to upgrade him to be able ' \
              f'to create new Animal objects'

    msg = f'From: {sender_email}\r\nTo: {admin_mail}\r\nContent-Type: text/plain; ' \
          f'charset="utf-8"\r\nSubject: {subject}\r\n\r\n' + message

    session = smtplib.SMTP_SSL(smtp_server, port)
    session.login(sender_email, password)
    session.sendmail(sender_email, admin_mail, msg.encode('utf-8'))
    session.quit()


def send_mail_change_status(user: User):
    if user.is_guest is False:
        subject = f'{user.username}: status upgraded'
        message = 'Your status was upgraded. You can now create and add new animal objects in your shelter'

    else:
        subject = f'{user.username}: status downgraded'
        message = 'Your status was downgraded. You can not now create and add new animal objects in your shelter'

    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    msg = f'From: {sender_email}\r\nTo: {user.email}\r\nContent-Type: text/plain; ' \
          f'charset="utf-8"\r\nSubject: {subject}\r\n\r\n' + message

    session = smtplib.SMTP_SSL(smtp_server, port)
    session.login(sender_email, password)
    session.sendmail(sender_email, user.email, msg.encode('utf-8'))
    session.quit()


