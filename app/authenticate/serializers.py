from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'is_company_owner', 'company', 'company_name', 'date_joined']
        read_only_fields = ['is_company_owner', 'company', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # Используем стандартный create метод ModelSerializer
        # и хешируем пароль вручную
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class AddEmployeeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if not data.get('user_id') and not data.get('email'):
            raise ValidationError("Необходимо указать user_id или email")
        return data