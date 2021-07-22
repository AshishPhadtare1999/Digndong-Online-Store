from django.db import models
from rest_framework import fields, serializers
from .models import Product

class ProductSerial(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
