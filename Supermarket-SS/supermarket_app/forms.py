from django import forms
from django.contrib.auth.models import User
from .models import Product


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_category',
                  'producer', 'price', 'quantity', 'image', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_category']
