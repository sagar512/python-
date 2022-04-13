from django.conf import settings
from django.core.mail import send_mail
import jwt
import datetime
from datetime import timezone
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import threading

class EmailSendThread(threading.Thread):
    def __init__(self, msg_subject, msg_body, to_email_list, from_email,
		attachment_list=None, **kwargs):
        self.msg_subject = msg_subject
        self.msg_body = msg_body
        self.from_email = from_email
        self.to_email_list = to_email_list
        self.extra_dict = kwargs
        self.attachment_list = attachment_list
        kwargs = {}  # empty it to prevent unknown keyword error
        super(EmailSendThread, self).__init__(**kwargs)

    def run(self):
        msg = EmailMultiAlternatives(self.msg_subject, self.msg_body,
            self.from_email, self.to_email_list)
        msg.attach_alternative(self.msg_body, "text/html")
        msg.send(True)


def send_mail_using_thread(msg_subject, msg_body, to_email_list, from_email,
		fail_silently=False, attachment_list=None):

    EmailSendThread(msg_subject, msg_body, to_email_list, from_email,
    	attachment_list=attachment_list, fail_silently=fail_silently,
    	html_message=msg_body).start()


def send_an_email(msg_subject, msg_body, to_email_list, from_email):
    email_list = to_email_list
    if type(to_email_list) is not list:
        email_list = [to_email_list]

    send_mail_using_thread(
        msg_subject=msg_subject,
        msg_body=msg_body,
        to_email_list=email_list,
        from_email=from_email)