from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
 
    def Integer(self):
        return self.user.id


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bakery', 'Bakery'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('beverages', 'Beverages')
    ]

    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=40, default="")
    product_category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES)
    producer = models.CharField(max_length=40, default="")
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='product_images/', verbose_name=_("Image"), null=True, blank=True)
