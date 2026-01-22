from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplyViewSet, SupplyReportView

router = DefaultRouter()
router.register(r'supplies', SupplyViewSet, basename='supply')

urlpatterns = [
    path('', include(router.urls)),
    path('report/', SupplyReportView.as_view(), name='supply-report'),
]