from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from user_app.models import User




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

#     def __str__(self):
#         return self.product.name

class Wallet(models.Model):
    wallet_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    wallet_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.wallet_user.username

class WalletHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00, null=True)
    type = models.CharField(max_length=255) # credit or debit
    date = models.DateTimeField(null=True)
    previous_wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00, null=True)
    current_wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00, null=True)

    def __str__(self):
        return self.user.username + ' ' + self.type

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + '    |    ' + self.product.name

# class Cart(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField()





# class Sale(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     date = models.DateTimeField(default=datetime.now)
#     price = models.DecimalField(max_digits=10, decimal_places=2)