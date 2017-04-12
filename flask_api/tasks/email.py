# -*- coding: utf-8 -*-

from flask import render_template
from flask_mail import Message
from flask_api.extensions import mail, celery


@celery.task
def send_welcome_email(email):
    """
    发送信息
    :return:
    """
    subject = '欢迎使用本系统！'
    content = '这是一封欢迎邮件，欢迎使用本系统！'
    send_email(
        subject=subject,
        recipients=[email],
        text_body=content,
        html_body=''
    )


@celery.task
def send_async_email(*args, **kwargs):
    send_email(*args, **kwargs)


def send_email(subject, recipients, text_body, html_body, sender=None):
    """Sends an email to the given recipients.

    :param subject: The subject of the email.
    :param recipients: A list of recipients.
    :param text_body: The text body of the email.
    :param html_body: The html body of the email.
    :param sender: A two-element tuple consisting of name and address.
                   If no sender is given, it will fall back to the one you
                   have configured with ``MAIL_DEFAULT_SENDER``.
    """
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
