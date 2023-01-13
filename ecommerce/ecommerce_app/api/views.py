from rest_framework import generics
from ecommerce_app.models import Customer, Product, Category, Brand
from ecommerce_app.api.serializers import UserSerializer, ProductSerializer, CartSerializer, OrderSerializer
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


# class AddAmountView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer

# class AddProductView(generics.CreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = ProductSerializer

class AddProductView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = (TokenAuthentication)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
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
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    




class ProductByCategoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(category=pk)



class ProductByBrandView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(brand=pk)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AdminOrReadOnly]

class AddToCartView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get('product_id'))
        if product.stock < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.stock -= 1
        serializer.data['quantity'] = 1
        product.save()
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        serializer.save(user=user)

class UpdateCartView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get('product_id'))
        if product.stock < self.request.data.get('quantity'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.stock -= self.request.data.get('quantity')
        serializer.data['quantity'] = self.request.data.get('quantity')
        product.save()
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(id=user_id)
        serializer.save(user=user)

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

