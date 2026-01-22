from rest_framework import serializers
from .models import Company, Storage


class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'inn', 'description', 'owner_email',
                  'employees_count', 'created_at']
        read_only_fields = ['owner_email', 'employees_count']

    @staticmethod
    def get_owner_email(obj):
        owner = obj.employees.filter(is_company_owner=True).first()
        return owner.email if owner else None


class StorageSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Storage
        fields = ['id', 'company', 'company_name', 'address', 'phone', 'created_at']