from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company', 'name', 'inn', 'contact_person', 'phone', 'email', 'address', 'created_at']
        read_only_fields = ['company']


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'inn', 'contact_person', 'phone', 'email', 'created_at']


