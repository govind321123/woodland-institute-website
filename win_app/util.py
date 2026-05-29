from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings


def sent_email(request, sender_name, from_mail, mail_subject, message_body):

    subject = mail_subject

    message = f"""
New Contact Message

Name: {sender_name}
Email: {from_mail}

Message:
{message_body}
"""

    mail = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        reply_to=[from_mail]
    )

    mail.send()


# -----------------------------
# FIX BAD ENCODING FROM ADMIN
# -----------------------------
def clean_text(text):

    if not text:
        return text

    replacements = {

        # Broken encoding symbols
        "ΓÇ£": "",
        "ΓÇ¥": "",
        "ΓÇÖ": "",
        "ΓÇô": "",
        "ΓÇö": "",

        # UTF-8 misinterpreted characters
        "â€™": "",
        "â€˜": "",
        "â€œ": "",
        "â€": "",
        "â€“": "",
        "â€”": "",

        # Other garbage symbols
        "â€¢": "",
        "â€¦": "",
        "â„¢": "",
        "Â©": "",
        "Â®": "",
        "Â ": " ",
        "ƒ": "",
        "�": "",
        "Â": "",
        "Ã": "",
        "â": "",
        "┬╜": "",
        "ÇÖs": "",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text



# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.conf import settings


# def sent_email(request, sender_name, from_mail, mail_subject, message_body):

#     subject = mail_subject

#     message = f"""
# New Contact Message

# Name: {sender_name}
# Email: {from_mail}

# Message:
# {message_body}
# """

#     mail = EmailMessage(
#         subject,
#         message,
#         settings.EMAIL_HOST_USER,     # sender (your Gmail)
#         [settings.EMAIL_HOST_USER],   # receiver (admin email)
#         reply_to=[from_mail]          # reply goes to user
#     )

#     mail.send()