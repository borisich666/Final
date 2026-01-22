from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserRegistrationSerializer, AddEmployeeSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_company_owner') and hasattr(user, 'company'):
            if user.is_company_owner and user.company:
                return User.objects.filter(company=user.company)
        return User.objects.filter(id=user.id)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class AddEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not hasattr(user, 'is_company_owner') or not user.is_company_owner:
            return Response(
                {'error': 'Только владелец компании может добавлять сотрудников'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not user.company:
            return Response(
                {'error': 'Вы не привязаны к компании'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AddEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = None

            if serializer.validated_data.get('user_id'):
                try:
                    employee = User.objects.get(id=serializer.validated_data['user_id'])
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Пользователь не найден'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            elif serializer.validated_data.get('email'):
                try:
                    employee = User.objects.get(email=serializer.validated_data['email'])
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Пользователь с таким email не найден'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            if not employee:
                return Response({'error': 'Пользователь не найден'}, status=404)

            if employee.is_company_owner:
                return Response(
                    {'error': 'Владелец компании не может быть добавлен как сотрудник'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if employee.company and employee.company != user.company:
                return Response(
                    {'error': 'Пользователь уже привязан к другой компании'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            employee.company = user.company
            employee.save()

            return Response(
                {'message': f'Пользователь {employee.email} успешно добавлен в компанию'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)