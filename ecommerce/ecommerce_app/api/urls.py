from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from ecommerce_app.api.views import (AddProductView, ProductListView, ProductByCategoryView,
                                     ProductByBrandView, ProductDetailView, AddToCartView, CartView, UpdateCartView)

urlpatterns = [
    path('addproduct/', AddProductView.as_view(), name='AddProduct'),
    path('productlist/', ProductListView.as_view(), name='ProductList'),
    path('productcategory/<int:pk>/', ProductByCategoryView.as_view(), name='ProductByCategory'),
    path('productbrand/<int:pk>/', ProductByBrandView.as_view(), name='ProductByBrand'),
    path('productdetail/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('addcart/', AddToCartView.as_view(), name='AddToCart'),
    path('cart/', CartView.as_view(), name='Cart'),
    path('updatecart/', UpdateCartView.as_view(), name='UpdateCart'),


    # path('api-auth/', include('rest_framework.urls')),
]