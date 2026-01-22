from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet, SalesAnalyticsView

router = DefaultRouter()
router.register(r'', SaleViewSet, basename='sale')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', SalesAnalyticsView.as_view(), name='sales-analytics'),
]