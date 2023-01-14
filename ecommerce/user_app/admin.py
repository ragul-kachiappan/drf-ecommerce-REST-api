from django.contrib import admin
from user_app.models import User
from ecommerce_app.models import  Category, Brand, Product, Order
# Register your models here.
admin.site.register(User)
# admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)