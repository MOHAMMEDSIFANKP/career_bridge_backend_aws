from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.contrib.sites.models import Site
from decouple import config

@shared_task
def send_activation_email(user_email, user_pk):
    # Construct and send the activation email
    user = User.objects.get(pk=user_pk)
    mail_subject = 'Please activate your account'
    message = render_to_string('user/activation_email.html', {
        'user': user,
        'domain': config('backendUrl'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'cite': config('backendUrl')
    })
    to_email = user_email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

@shared_task
def send_forgotpassword_email(email):
    user = User.objects.get(email=email)
    mail_subject = 'Reset your password'
    message = render_to_string('user/forgot_password.html', {
        'user': user,
        'domain': config('backendUrl'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'cite': config('backendUrl')
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
