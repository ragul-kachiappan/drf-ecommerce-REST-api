from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from user_app.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brands")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

# class Cart(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField()

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)
#     date = models.DateTimeField(default=datetime.now)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

# class WalletHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=255) # credit or debit
#     date = models.DateTimeField(default=datetime.now)

# class Sale(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     date = models.DateTimeField(default=datetime.now)
#     price = models.DecimalField(max_digits=10, decimal_places=2)