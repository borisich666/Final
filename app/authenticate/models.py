from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_company_owner = models.BooleanField(default=False, verbose_name='Владелец компании')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='employees', verbose_name='Компания')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.email}"

    def clean(self):
        if self.is_company_owner and self.company:
            raise ValidationError('Владелец компании не может быть привязан к существующей компании')

    def save(self, *args, **kwargs):
        if self.is_company_owner:
            self.company = None
        super().save(*args, **kwargs)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название компании')
    inn = models.CharField(max_length=12, unique=True, verbose_name='ИНН')
    description = models.TextField(blank=True, verbose_name='Описание компании')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f"{self.name}"


class Storage(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE,
                                   related_name='storage', verbose_name='Компания')
    address = models.CharField(max_length=500, verbose_name='Адрес склада')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f"Склад: {self.address}"


class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='suppliers', verbose_name='Компания')
    name = models.CharField(max_length=255, verbose_name='Название поставщика')
    inn = models.CharField(max_length=12, verbose_name='ИНН поставщика')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        unique_together = ['company', 'inn']


class Product(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE,
                                related_name='products', verbose_name='Склад')
    name = models.CharField(max_length=255, verbose_name='Название товара')
    sku = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Закупочная цена')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name='Цена продажи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name}"


class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,
                                 related_name='supplies', verbose_name='Поставщик')
    delivery_date = models.DateField(default=timezone.now, verbose_name='Дата поставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'


class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE,
                               related_name='supply_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='supply_products')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                           verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставках'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product.quantity += self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)


class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='sales', verbose_name='Компания')
    buyer_name = models.CharField(max_length=255, verbose_name='Имя покупателя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'


class ProductSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE,
                             related_name='sale_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sale_products')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                           verbose_name='Количество')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name='Цена продажи')

    class Meta:
        verbose_name = 'Товар в продаже'
        verbose_name_plural = 'Товары в продажах'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.product.quantity < self.quantity:
                raise ValidationError(
                    f'Недостаточно товара "{self.product.name}" на складе'
                )
            self.product.quantity -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)