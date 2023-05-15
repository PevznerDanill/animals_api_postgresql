from .models import User
from django.conf import settings
from .models import User
import smtplib


def send_email_to_upgrade(user: User) -> None:
    """
    Generates an email message to inform the admin that the user asked to upgrade his status
    and sends it to the email saved in the superuser's instance.
    """
    admin_mail = User.objects.only('email').get(is_superuser=True).email
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    subject = 'New request to upgrade user'

    message = f'The user {user.username} with id {user.id} asks to upgrade him to be able ' \
          f'to create new Animal objects and set the is_guest flag to False. If you decide to ' \
          f'accept the request and then in the future to set the flag back to True, do not forget to also' \
          f'set the flag asked_for_upgrade so the user could send a new request.'

    msg = f'From: {sender_email}\r\nTo: {admin_mail}\r\nContent-Type: text/plain; ' \
          f'charset="utf-8"\r\nSubject: {subject}\r\n\r\n' + message

    session = smtplib.SMTP_SSL(smtp_server, port)
    session.login(sender_email, password)
    session.sendmail(sender_email, admin_mail, msg.encode('utf-8'))
    session.quit()


def send_mail_change_status(user: User) -> None:
    """
    Generates an email message to inform the user that his status was changed and sends it to him.
    """
    if not user.email:
        return

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


