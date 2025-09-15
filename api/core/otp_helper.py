import base64
from enum import Enum
from random import randint
from django.conf import settings


class OTPtypes(Enum):
    CREATE_USER = "create"
    FORGOT_PASSWORD = "forgot"
    CHANGE_MOBILE = "change_mobile"

    @staticmethod
    def get_enum_set():
        return set(item.value for item in OTPtypes)

    @staticmethod
    def choices():
        return [(item.value, item.value) for item in OTPtypes]


class OTPSendTypes(Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"

    @staticmethod
    def get_enum_set():
        return set(item.value for item in OTPSendTypes)

    @staticmethod
    def choices():
        return [(item.value, item.value) for item in OTPSendTypes]

    @staticmethod
    def get_mobile_choices():
        return [
            (item.value, item.value)
            for item in OTPSendTypes
            if item.value in ["sms", "whatsapp"]
        ]


def get_random_otp():
    if settings.IS_RANDOM_OTP:
        return str(randint(1000, 9999))
    return settings.DEFAULT_OTP


def get_otp_verified_token(otp, email):
    token_str = get_random_otp() + email + otp
    token_str_bytes = token_str.encode("ascii")
    base64_bytes = base64.b64encode(token_str_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message
