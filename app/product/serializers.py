from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    storage_address = serializers.CharField(source='storage.address', read_only=True)
    company_name = serializers.CharField(source='storage.company.name', read_only=True)
    profit_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'storage', 'storage_address', 'company_name', 'name',
                  'description', 'sku', 'quantity', 'purchase_price', 'sale_price',
                  'min_quantity', 'profit_per_unit', 'created_at', 'updated_at']
        read_only_fields = ['quantity']


class ProductListSerializer(serializers.ModelSerializer):
    storage_address = serializers.CharField(source='storage.address', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'quantity',
                  'purchase_price', 'sale_price', 'storage_address',
                  'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['storage', 'name', 'description', 'sku',
                  'purchase_price', 'sale_price', 'min_quantity']

    def validate(self, data):
        # При создании товара quantity всегда 0
        data['quantity'] = 0
        return data