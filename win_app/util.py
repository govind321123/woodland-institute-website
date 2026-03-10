from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings 


def sent_email(request, sender_name, from_mail, mail_subject, message_body):
  current_site = get_current_site(request)

  mail = EmailMessage(mail_subject, message_body, from_mail, to=[settings.EMAIL_HOST_USER])
  mail.send()
