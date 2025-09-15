from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def send_confirmation_code(new_otp):
    send_mail("Generated OTP", f"Here is your otp: {new_otp.code}", settings.EMAIL_HOST_USER, [new_otp.identifier])


def send_admin_error(subject, message, err_from):
    superusers = User.objects.filter(is_superuser=True)
    send_mail(f"{subject}", f"Error: {message} From:{err_from}", settings.EMAIL_HOST_USER, [user.email for user in superusers])
