from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import Seller, User
from .models import Category


class CategoryTest(APITestCase):
    def add_category(self, name: str, description: str):
        url = reverse('products:category-list')
        User.objects.create_superuser(username='admin', password='12345')
        self.client.login(username='admin', password='12345')
        data = {
            'name': name,
            'description': description
        }
        return self.client.post(path=url, data=data, format='json')

    def test_add_category(self):
        response = self.add_category(name='Laptops', description='Description for Laptops category')
        expected_result = {
            "new_category": {
                "id": 1,
                "name": "Laptops",
                "description": "Description for Laptops category",
                "parent": None
            }
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = response.json()
        self.assertDictEqual(response, expected_result)


class ProductTest(APITestCase):
    def setUp(self) -> None:
        Seller.objects.create_user(username='seller', password='12345')
        self.client.login(username='seller', password='12345')

    def add_product(self, name: str, category: str, price: float, quantity: int):
        url = reverse('products:product_list')
        data = {
            'name': name,
            'category': category,
            'price': price,
            'quantity': quantity
        }
        return self.client.post(path=url, data=data, format='json')

    def test_add_product(self):
        Category.objects.create(name='Laptops', description='Description for Laptops category')
        response = self.add_product(name='MacBook Pro', category='Laptops', price=1234.56, quantity=10)
        expected_result = {
            "new_product": {
                "id": 1,
                "category": "Laptops",
                "owner": "seller",
                "name": "MacBook Pro",
                "price": '1234.56',
                "quantity": 10,
                "is_active": True
            }
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = response.json()
        self.assertDictEqual(response, expected_result)
