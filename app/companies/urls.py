from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, StorageViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'storages', StorageViewSet, basename='storage')

urlpatterns = [
    path('', include(router.urls)),
]