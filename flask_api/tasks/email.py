# -*- coding: utf-8 -*-

"""
    发送邮件任务
"""

from flask_mail import Message
from flask_api.extensions import mail, celery


@celery.task
def send_welcome_email(recipient):
    """
    发送信息
    :return:
    """
    subject = '欢迎使用本系统！'
    content = '这是一封欢迎邮件，欢迎使用本系统！'
    send_email(
        subject=subject,
        recipients=[recipient],
        text_body=content,
        html_body=''
    )


def send_email(subject, recipients, text_body, html_body, sender=None):
    """
    发送邮件给指定的用户
    :param subject:     邮件主题
    :param recipients:  邮件收件人列表
    :param text_body:   邮件正文
    :param html_body:   邮件html
    :param sender:      发送者
    :return:
    """
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
