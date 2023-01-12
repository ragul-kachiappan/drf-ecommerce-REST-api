from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import SignUpView, AddAdminView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('addadmin/', AddAdminView.as_view(), name='addadmin'),

    # path('api-auth/', include('rest_framework.urls')),
]