from rest_framework import serializers

from product.serializers import ProductListSerializer
from .models import Supply, SupplyProduct


class SupplyProductSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)

    class Meta:
        model = SupplyProduct
        fields = ['id', 'product', 'product_details', 'quantity', 'purchase_price']


class SupplySerializer(serializers.ModelSerializer):
    supply_products = SupplyProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Supply
        fields = ['id', 'supplier', 'supplier_name', 'delivery_date',
                  'created_at', 'notes', 'supply_products', 'total_quantity', 'total_cost']


class CreateSupplySerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def validate(self, data):
        # Проверяем поставщика
        from suppliers.models import Supplier
        try:
            supplier = Supplier.objects.get(id=data['supplier_id'])
        except Supplier.DoesNotExist:
            raise serializers.ValidationError("Поставщик не найден")

        # Проверяем товары
        from product.models import Product
        for product_item in data['products']:
            product_id = product_item.get('id')
            quantity = product_item.get('quantity')

            if not product_id or not quantity:
                raise serializers.ValidationError("Каждый товар должен иметь id и quantity")

            if quantity <= 0:
                raise serializers.ValidationError("Количество товара должно быть положительным")

            try:
                Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Товар с id {product_id} не найден")

        return data


class SupplyInvoiceSerializer(serializers.Serializer):
    supplier = serializers.CharField()
    inn = serializers.CharField()
    delivery_date = serializers.DateField()
    accepted_by = serializers.CharField()
    products = serializers.DictField(child=serializers.IntegerField())