from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('authenticate.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/product/', include('product.urls')),
    path('api/warehouse/', include('warehouse.urls')),
    path('api/sales/', include('sales.urls')),
]