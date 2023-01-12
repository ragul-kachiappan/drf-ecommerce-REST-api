from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from user_app.models import User
from user_app.api.serializers import SignUpSerializer, AddAdminSerializer

# class SignUpView(generics.CreateAPIView):
#     serializer_class = SignUpSerializer

#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             data = {}
#             data['Response'] = "Registration successful"
#             data['username'] = serializer.data['username']
#             account = User(email=serializer.validated_data['email'], username=serializer.validated_data['username'])
#             token = Token.objects.get_or_create(user=account).key
#             serializer.save(is_active=True)
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)



# class AddAdminView(generics.CreateAPIView):
#     serializer_class = SignUpSerializer
#     permission_classes = (IsAuthenticated, IsAdminUser)

#     def perform_create(self, serializer):
#         serializer.save(is_admin=True, is_active=True, is_staff=True)

#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             data = {}
#             data['Response'] = "Registration successful"
#             data['username'] = serializer.data['username']
#             account = User(email=serializer.validated_data['email'], username=serializer.validated_data['username'])
#             # token = Token.objects.get(user=account).key
#             serializer.save(is_admin=True, is_active=True, is_staff=True)
#         else:
#             data = serializer.errors
#         return Response(data)


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data = {}
        data['Response'] = "Registration successful"
        data['username'] = user.username
        data['token'] = token
        return Response(data)

class AddAdminView(APIView):
    def post(self, request):
        serializer = AddAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data = {}
        data['Response'] = "Registration successful"
        data['username'] = user.username
        data['token'] = token
        return Response(data)

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user).key
            data = {}
            data['Response'] = "Login successful"
            data['username'] = user.username
            data['token'] = token
            return Response(data)
        else:
            data = {}
            data['Response'] = "Invalid credentials"
            return Response(data)





# @api_view(['POST',])
# def signup_view(request):

#     if request.method == 'POST':
#         serializer = SignUpSerializer(data=request.data)

#         data = {}
#         if serializer.is_valid():
#             account = serializer.save(is_admin=False, is_active=True, is_staff=False, is_superuser=False)
#             data['response'] = "Registration Successful!"
#             data['username'] = account.username
#             data['email'] = account.email
            
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)

# @api_view(['POST',])
# def add_admin_view(request):

#     if request.method == 'POST':
#         serializer = SignUpSerializer(data=request.data)

#         data = {}
#         if serializer.is_valid():
#             account = serializer.save(is_admin=True, is_active=True, is_staff=True, is_superuser=False)
#             data['response'] = "Registration Successful!"
#             data['username'] = account.username
#             data['email'] = account.email
            
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)