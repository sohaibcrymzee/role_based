from django.db import models
from django.utils.translation import gettext as _


class Condition(models.TextChoices):
    NEW = "new", _("NEW")
    USED = "used", _("USED")


class WEIGHTUNIT(models.TextChoices):
    G = "g", _("g")
    KG = "kg", _("kg")
    LB = "lb", _("lb")
    OZ = "oz", _("oz")
    YARD = "yd", _("yd")


class DIMMENSIONUNIT(models.TextChoices):
    CENTEMETER = "cm", _("cm")
    INCH = "in", _("in")
    FOOT = "ft", _("ft")
    METER = "m", _("m")
    MILIMETER = "mm", _("mm")


class TransmissionTypes(models.TextChoices):
    AUTOMATIC = "auto", _("AUTO")
    MANUAL = "manual", _("MANUAL")
    SEMIAUTO = "semi_auto", _("SEMI_AUTO")
    CVT = "cvt", _("CVT")


class ShippingType(models.TextChoices):
    MANUAL_SHIPPING = "mannual_shipping", _("MANNUAL_SHIPPING")
    AUTO_SHIPPING = "auto_shipping", _("AUTO_SHIPPING")
