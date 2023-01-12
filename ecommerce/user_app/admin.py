from django.contrib import admin
from user_app.models import User
from ecommerce_app.models import Customer, Category, Brand, Product
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)