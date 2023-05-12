from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bakery', 'Bakery'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('beverages', 'Beverages'),
        ('dairy', 'Dairy'),
        ('meats', 'Meats'),
        ('coffe & tea', 'Coffe & Tea'),
        ('cans & jars', 'Cans & Jars'),
        ('herbs & spices', 'Herbs & Spices'),
        ('frozen', 'Frozen'),
        ('hygiene', 'Hygiene')

    ]

    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=40, default="")
    product_category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES)
    producer = models.CharField(max_length=40, default="")
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    description = models.TextField(default="")
    date_added = models.DateField(auto_now_add=True)
    image = models.ImageField(
        upload_to='product_images/', verbose_name=_("Image"), null=True, blank=True)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username

    def Integer(self):
        return self.user.id


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)


class OrderedProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Reviews(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(default="")
