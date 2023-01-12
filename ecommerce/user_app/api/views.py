from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from user_app.models import User
from user_app.api.serializers import SignUpSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=True)

class AddAdminView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(is_admin=True, is_active=True, is_staff=True, is_superuser=True)

