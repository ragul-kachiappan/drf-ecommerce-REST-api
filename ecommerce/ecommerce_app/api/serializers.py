from rest_framework import serializers
from ecommerce_app.models import Product, Category, Brand, Order, Wallet, WalletHistory


class ProductGetSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['name', 'category_name', 'brand_name', 'price', 'stock', 'description']

class ProductPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'price', 'stock', 'description']


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
        fields = ['product', 'product_name', 'quantity', 'purchase_date', 'total_price']

class WalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletHistory
        fields = ['id', 'amount', 'type', 'previous_wallet_amount', 'current_wallet_amount', 'date']

# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sale
#         fields = ['id', 'product', 'date', 'price']