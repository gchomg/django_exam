from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category = models.CharField(max_length=100, blank=True, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} ({self.sku})'

    def clean(self):
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Название не может быть пустым.'})
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'Цена должна быть больше 0.'})
        qs = Product.objects.filter(sku=self.sku)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({'sku': 'Товар с таким артикулом уже существует.'})
