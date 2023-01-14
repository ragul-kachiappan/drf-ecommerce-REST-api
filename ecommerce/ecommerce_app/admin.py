from django.contrib import admin
from ecommerce_app.models import  Category, Brand, Product, Order, Wallet, WalletHistory
# Register your models here.

# admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(WalletHistory)
