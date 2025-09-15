from django.conf import settings
from twilio.rest import Client
from rest_framework import status
from api.core.utils import DotsValidationError


class TwilioService:
    def __init__(self) -> None:
        pass

    def send_sms(phone_number, **kwargs):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        except Exception as e:
            raise DotsValidationError({'error':["unable to send otp"]})
        message = kwargs.get("message")
        message_type = kwargs.get("message_type")

        is_twilio_enabled = settings.IS_TWILIO_ENABLED

        if is_twilio_enabled:
            if message_type == "whatsapp":
                try:
                    client.messages.create(
                        body=message,
                        from_="whatsapp:{wfrom}".format(
                            wfrom=settings.TWILIO_WHATSAPP_PHONE_NUMBER
                        ),
                        to="whatsapp:{phone}".format(phone=phone_number),
                    )
                except Exception as e:
                    print(str(e))
                    raise DotsValidationError({'otp':["unable to send otp"]})
            else:
                try:
                    client.messages.create(
                        body=message, from_=settings.TWILIO_PHONE_NUMBER, to=phone_number
                    )
                except Exception as e:
                    print(str(e))
                    raise DotsValidationError({'otp':["unable to send otp"]})