from rest_framework import serializers
from django.db import transaction
from .models import Sale, ProductSale


class SimpleProductSerializer(serializers.Serializer):
    """Упрощенный сериализатор для товаров"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    sku = serializers.CharField()
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProductSaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductSale
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity',
                  'sale_price', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.sale_price


class SaleSerializer(serializers.ModelSerializer):
    sale_products = ProductSaleSerializer(many=True)
    total_amount = serializers.SerializerMethodField()
    total_profit = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'company', 'buyer_name', 'buyer_phone', 'buyer_email',
                  'discount', 'created_at', 'total_amount', 'total_profit', 'sale_products']
        read_only_fields = ['company']

    def get_total_amount(self, obj):
        total = sum(item.quantity * item.sale_price for item in obj.sale_products.all())
        return total * (1 - obj.discount / 100)

    def get_total_profit(self, obj):
        total = 0
        for item in obj.sale_products.all():
            total += item.quantity * (item.sale_price - item.product.purchase_price)
        return total * (1 - obj.discount / 100)

    @transaction.atomic
    def create(self, validated_data):
        sale_products_data = validated_data.pop('sale_products')
        sale = Sale.objects.create(**validated_data)

        for product_data in sale_products_data:
            ProductSale.objects.create(sale=sale, **product_data)

        return sale