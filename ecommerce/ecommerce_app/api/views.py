from rest_framework import generics
from ecommerce_app.models import Customer, Product, Category, Brand
from ecommerce_app.api.serializers import UserSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from ecommerce_app.api.custom_permissions import AdminOrReadOnly, UserOrReadOnly
from rest_framework.response import Response
from rest_framework import status


# class AddAmountView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer

# class AddProductView(generics.CreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = ProductSerializer

class AddProductView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductByCategoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(category=pk)

class ProductByBrandView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(brand=pk)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AdminOrReadOnly]

