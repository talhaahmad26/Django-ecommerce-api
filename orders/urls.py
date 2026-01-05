from rest_framework.routers import DefaultRouter
from . import views
from .views import OrderViewSet, CartViewSet
from django.urls import path,include

router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
