from django.shortcuts import render
from .models import Category,Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets
# Create your views here.

class category_viewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class product_viewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    