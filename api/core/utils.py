import logging

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.views import exception_handler


User = get_user_model()
logger = logging.getLogger("stocksmaze")


class DotsValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "non_field"
    key = "validations"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = {"non_field": [detail]}

        self.detail = _get_error_details(detail, code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and type(exc):
        if response.data.get("detail"):
            custom_response = dict(
                key="validations", messages={"non_field": [response.data["detail"]]}
            )
        elif response.data.get("non_field_errors"):
            custom_response = dict(
                key="validations",
                messages={"non_field": [response.data["non_field_errors"]]},
            )
        else:
            custom_response = dict(key="validations", messages=response.data)
        response.data = custom_response
        return response

    return response




def calculate_cart_total(items):
    data = {"sub_total": 0, "delivery_charges": 0, "store_tax": 0, "total": 0}
    for item in items:
        product = item.product
        quantity = item.quantity
        price = product.sale_price if product.is_sale_price else product.price
        subtotal = price * quantity
        delivery_charges = product.delivery_charges  # Fixed attribute name
        total = subtotal + delivery_charges
        data["sub_total"] += subtotal
        data["delivery_charges"] += delivery_charges
        data["total"] += total
    return data
