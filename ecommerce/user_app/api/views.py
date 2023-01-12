from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from user_app.models import User
from user_app.api.serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user_type = self.request.data.get('user_type')
        if user_type == 'customer':
            serializer.save(is_customer=True)
        elif user_type == 'admin':
            raise ValidationError("Need to be registered via add admin panel by an existing superuser!")

class AddAdminView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(is_admin=True)