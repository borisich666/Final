from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    # Временно уберем queryset и определим его в get_queryset
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_obj = self.request.user

        if hasattr(user_obj, 'is_company_owner') and hasattr(user_obj, 'company'):
            if user_obj.is_company_owner and user_obj.company:
                return User.objects.filter(company=user_obj.company)

        return User.objects.filter(id=user_obj.id)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and hasattr(user_obj, 'is_company_owner'):
            if user_obj.company or user_obj.is_company_owner:
                raise serializers.ValidationError(
                    'Вы уже связаны с компанией'
                )
        else:
            raise PermissionDenied('Неверный тип пользователя')

        company = serializer.save()

        if hasattr(user_obj, 'is_company_owner'):
            user_obj.is_company_owner = True
            user_obj.save()


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and user_obj.company:
            return Storage.objects.filter(company=user_obj.company)

        return Storage.objects.none()


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and user_obj.company:
            return Supplier.objects.filter(company=user_obj.company)

        return Supplier.objects.none()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and user_obj.company:
            return Product.objects.filter(storage__company=user_obj.company)

        return Product.objects.none()


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and user_obj.company:
            return Supply.objects.filter(supplier__company=user_obj.company)

        return Supply.objects.none()


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = self.request.user

        if hasattr(user_obj, 'company') and user_obj.company:
            return Sale.objects.filter(company=user_obj.company)

        return Sale.objects.none()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class AnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_obj = request.user

        if not hasattr(user_obj, 'company'):
            return Response(
                {'error': 'Неверный тип пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user_obj.company:
            return Response(
                {'error': 'Вы не привязаны к компании'},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(storage__company=user_obj.company)
        sales = Sale.objects.filter(company=user_obj.company)

        total_revenue = ProductSale.objects.filter(
            sale__company=user_obj.company
        ).aggregate(
            total=models.Sum(models.F('quantity') * models.F('sale_price'))
        )['total'] or 0

        return Response({
            'total_products': products.count(),
            'total_sales': sales.count(),
            'total_revenue': float(total_revenue)
        })