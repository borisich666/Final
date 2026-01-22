from django.db import models
from django.contrib.auth.models import AbstractUser
from companies.models import Company


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_company_owner = models.BooleanField(default=False, verbose_name='Владелец компании')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='employees', verbose_name='Компания')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'

    def __str__(self):
        return f"{self.email}"

    def clean(self):
        if self.is_company_owner and self.company:
            from django.core.exceptions import ValidationError
            raise ValidationError('Владелец компании не может быть привязан к существующей компании')