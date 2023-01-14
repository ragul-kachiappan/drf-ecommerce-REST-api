from rest_framework import serializers
from ecommerce_app.models import Product, Category, Brand, Order

# class CustomerSerializer(serializers.ModelSerializer):
#     cart = serializers.ListField()
#     class Meta:
#         model = Customer
#         fields = ['username', 'first_name', 'last_name', 'email', 'wallet_balance']

class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['name', 'category_name', 'brand_name', 'price', 'stock', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['id', 'product', 'user', 'quantity']

class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product']

class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'quantity', 'date', 'total_price']

# class WalletHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WalletHistory
#         fields = ['id', 'user', 'amount', 'type', 'date']

# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sale
#         fields = ['id', 'product', 'date', 'price']