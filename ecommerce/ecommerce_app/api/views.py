from rest_framework import generics
from ecommerce_app.models import Product, Category, Brand, Order, Wallet, WalletHistory
from ecommerce_app.api.serializers import (ProductGetSerializer, ProductPostSerializer, OrderSerializer, AddCartSerializer,
                                        UpdateCartSerializer, WalletHistorySerializer)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from ecommerce_app.api.custom_permissions import AdminOrReadOnly, UserOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from user_app.models import User
from rest_framework.exceptions import ValidationError
from decimal import Decimal
import datetime

# class AddAmountView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer

# class AddProductView(generics.CreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = ProductSerializer

# class AddToWalletView(generics.CreateAPIView):
#     serializer_class = WalletSerializer
#     permission_classes = (IsAuthenticated,)

#     def perform_create(self, serializer):
#         user_id = Token.objects.get(key=self.request.auth.key).user_id
#         user = User.objects.get(id=user_id)
#         user_wallet, created = Wallet.objects.get_or_create(wallet_user=user)
#         print(self.request.data.get('amount'))
#         new_balance = user_wallet.wallet_balance
#         serializer.save(wallet_user = user, wallet_balance = new_balance)
#         return Response({'Wallet balance': new_balance}, status=status.HTTP_200_OK)

class AddToWalletView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def put(self,request):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        user_wallet, created = Wallet.objects.get_or_create(wallet_user=user)
        wallet_record = WalletHistory.objects.create(user=user)
        wallet_record.previous_wallet_amount = user_wallet.wallet_balance
        wallet_record.type = "credit"
        wallet_record.amount = Decimal(self.request.data.get('amount'))
        user_wallet.wallet_balance += Decimal(self.request.data.get('amount'))
        wallet_record.current_wallet_amount = user_wallet.wallet_balance
        wallet_record.date = datetime.datetime.now()
        user_wallet.save()
        wallet_record.save()
        data = {
            'user' : user.username,
            'wallet_balance': user_wallet.wallet_balance
        }
        return Response(data, status=status.HTTP_200_OK)

class AddProductView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        serializer = ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            object = serializer.save()
            data = {}
            data['id'] = object.id
            data['name'] = object.name
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer
    pagination_class = PageNumberPagination
    




class ProductByCategoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProductGetSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        pk = self.request.data['category_id']
        return Product.objects.filter(category=pk)



class ProductByBrandView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProductGetSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        pk = self.request.data['brand_id']
        return Product.objects.filter(brand=pk)



class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        pk = self.request.data['product_id']
        product = Product.objects.get(id=pk)
        serializer = ProductGetSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AddToCartView(generics.CreateAPIView):
    serializer_class = AddCartSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get('product'))
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        if product.stock < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(user=user, product=product)
        if order.exists():
            raise ValidationError("You have already added this product to your cart")
        product.stock -= 1
        product.save()

        serializer.save(user = user, quantity = 1, total_price = product.price)
        data = {
            'user': user.username,
            'product': product.name,
            'message': "Product added to your cart"
        }

        return Response(data, status=status.HTTP_201_CREATED)
    

class CartView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        cart = Order.objects.filter(user=user)
        serializer = OrderSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCartView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request):
        product = get_object_or_404(Product, pk=self.request.data.get('product'))
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        order = Order.objects.filter(user=user, product=self.request.data.get('product'))
        if order.exists():
            order.update(quantity = self.request.data.get('quantity'))
            order.update(total_price = self.request.data.get('quantity') * product.price)
            data = {
                'user': user.username,
                'product': product.name,
                'quantity': self.request.data.get('quantity')
            }
            product.stock -= (self.request.data.get('quantity') - 1)
            product.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Item not in cart")



class BuyCartView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user=user, purchased=False)
        wallet = get_object_or_404(Wallet, wallet_user=user)
        wallet_record = WalletHistory.objects.create(user=user)

        total_bill = sum([order.total_price for order in orders.all()])
        if total_bill > wallet.wallet_balance:
            return Response(
                {'error': 'Insufficient balance in wallet'},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        wallet_record.previous_wallet_amount = wallet.wallet_balance
        wallet_record.amount = total_bill
        wallet_record.type = "debit"
        wallet.wallet_balance -= total_bill
        wallet_record.current_wallet_amount = wallet.wallet_balance
        wallet_record.date = datetime.datetime.now()
        wallet.save()
        wallet_record.save()
        for order in orders.all():
            order.purchased = True
            order.purchase_date = datetime.datetime.now()
            order.save()
        return Response({'success': 'Order placed successfully'})



class WalletHistoryView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)    
    serializer_class = WalletHistorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination    
    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        return WalletHistory.objects.filter(user=user, date__gte=self.request.data['from_date'], date__lte=self.request.data['to_date'])

class OrderHistoryView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)    
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        return Order.objects.filter(user = user, purchased = True)






# class UpdateCartView(generics.UpdateAPIView):
#     serializer_class = UpdateCartSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         user_id = Token.objects.get(key=self.request.auth.key).user_id
#         user = User.objects.get(id=user_id)
#         return Order.objects.filter(user=user, product=self.request.data['product'])

#     def perform_update(self, serializer):
#         product = get_object_or_404(Product, pk=self.request.data.get('product_id'))
#         if product.stock < self.request.data.get('quantity'):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         order = Order.objects.filter(user=user, product=product)
#         if order.exists():
#             product.stock -= (self.request.data.get('quantity') - 1)
#             product.save()
#             serializer.save(user=user, quantity= self.request.data.get('quantity'), total_price= product.price * self.request.data.get('quantity'))
#             data = {
#                 'user': user.name,
#                 'product': product.name,
#                 'quantity': self.request.data.get('quantity'),
#                 'message': "Product quantity updated successfully"
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             raise ValidationError('You have not added this product your cart')






# class DisplayCartView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = (IsAuthenticated,)
#     pagination_class = None
#     def get_queryset(self):
#         user_id = Token.objects.get(key=self.request.auth.key).user_id
#         user = User.objects.get(id=user_id)
#         return Order.objects.filter(user=user)






# class BuyCartView(generics.UpdateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = (IsAuthenticated,)

#     def perform_update(self, serializer):
#         user = self.request.user
#         wallet, created = Wallet.objects.get_or_create(user=user)
#         order = get_object_or_404(Order, customer=user, purchased=False)
#         total_price = sum([product.price for product in order.products.all()])
#         if wallet.balance < total_price:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         wallet.balance -= total_price
#         wallet.save()
#         order.purchased = True
#         order.save()
#         serializer.save()



