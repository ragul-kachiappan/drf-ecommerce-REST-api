from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from ecommerce_app.api.views import (AddProductView, ProductListView, ProductByCategoryView,
                                     ProductByBrandView, ProductDetailView, AddToCartView, CartView,
                                    UpdateCartView, AddToWalletView, BuyCartView, WalletHistoryView,
                                    OrderHistoryView, RemoveFromCartView, SaleReportByDateView, SaleReportByBrandView)

urlpatterns = [
    path('addproduct/', AddProductView.as_view(), name='AddProduct'),
    path('productlist/', ProductListView.as_view(), name='ProductList'),
    path('productcategory/', ProductByCategoryView.as_view(), name='ProductByCategory'),
    path('productbrand/', ProductByBrandView.as_view(), name='ProductByBrand'),
    path('productdetail/', ProductDetailView.as_view(), name='product'),
    path('addcart/', AddToCartView.as_view(), name='AddToCart'),
    path('cart/', CartView.as_view(), name='Cart'),
    path('updatecart/', UpdateCartView.as_view(), name='UpdateCart'),
    path('removecart/', RemoveFromCartView.as_view(), name='Remove'),
    path('addtowallet/', AddToWalletView.as_view(), name='AddToWallet'),
    path('buycart/', BuyCartView.as_view(), name='BuyCart'),
    path('wallethistory/', WalletHistoryView.as_view(), name='WalletHistory'),
    path('orderhistory/', OrderHistoryView.as_view(), name='OrderHistory'),
    path('salereportbydate/', SaleReportByDateView.as_view(), name='SaleReportByDate'),
    path('salereportbybrand/', SaleReportByBrandView.as_view(), name='SaleReportByBrand'),


    # path('api-auth/', include('rest_framework.urls')),
]