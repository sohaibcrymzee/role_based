from django.db import models
from api.core.models import  BaseModel

# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=200)