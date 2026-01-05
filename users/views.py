from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import RegisterSerializer
from .models import User

# Create your views here.
# SIGNUP VIEW
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]