from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authenticate.views import RegisterView, AnalyticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authenticate.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/analytics/', AnalyticsView.as_view(), name='analytics'),
]
