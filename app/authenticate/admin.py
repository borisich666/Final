from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_company_owner', 'company')
    list_filter = ('is_company_owner', 'company')
    search_fields = ('email', 'username')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'created_at')
    search_fields = ('name', 'inn')

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('company', 'address', 'created_at')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'company', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'purchase_price', 'sale_price')

class SupplyProductInline(admin.TabularInline):
    model = SupplyProduct
    extra = 1

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'delivery_date', 'created_at')
    inlines = [SupplyProductInline]

class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'buyer_name', 'created_at')
    inlines = [ProductSaleInline]