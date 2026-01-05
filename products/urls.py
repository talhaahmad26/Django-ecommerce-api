from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categoryapi', views.category_viewset)
router.register('productapi', views.product_viewset)

urlpatterns = [
    path('', include(router.urls)),
]


