from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from .models import Product


class PingTest(TestCase):
    def test_ping_returns_200(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)


class ProductCRUDTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Тестовый товар',
            category='Тест',
            price=Decimal('99.99'),
            sku='SKU-001',
        )

    def test_list_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        response = self.client.post(reverse('create'), {
            'name': 'Новый товар',
            'category': 'Электроника',
            'price': '199.00',
            'sku': 'SKU-002',
        })
        self.assertEqual(response.status_code, 302)

    def test_create_duplicate_sku(self):
        response = self.client.post(reverse('create'), {
            'name': 'Дубль',
            'category': 'Тест',
            'price': '50.00',
            'sku': 'SKU-001',
        })
        self.assertEqual(response.status_code, 200)

    def test_404_on_missing_product(self):
        response = self.client.get('/9999/update/')
        self.assertEqual(response.status_code, 404)

    def test_delete_product(self):
        response = self.client.post(reverse('delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
