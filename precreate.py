import requests
from urllib.parse import urljoin
from decimal import Decimal
from random import uniform, randint
import json


class StoreFiller:
    hostname = 'http://localhost:8000/api/v1/'
    MIN_VALUE_FOR_PRICE = 1.00
    MAX_VALUE_FOR_PRICE = 50000.00
    MIN_QUANTITY = 10
    MAX_QUANTITY = 100

    def __init__(self, username: str, password: str, session: requests.Session = None):
        self.session = session or requests.Session()
        self.username = username
        self.password = password

    def get(self, url):
        self.session.get(url, auth=(self.username, self.password))

    def post(self, url, data):
        self.session.post(url, data=data, auth=(self.username, self.password))

    def create_category(self, name: str, description: str):
        self.post(url=urljoin(self.hostname, 'categories'), data={'name': name, 'description': description})

    def create_product(self, name: str, category: str, price=None, quantity=None) -> None:
        if price is None:
            price = self.__random_price()
        if quantity is None:
            quantity = self.__random_quantity()
        self.post(url=urljoin(self.hostname, 'products'), data={'name': name,
                                                                'category': category,
                                                                'price': price,
                                                                'quantity': quantity,
                                                                'owner': self.username
                                                                })

    def load_categories_from_json(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data = json.load(file)
            for category in data['categories']:
                self.create_category(name=category, description=f'Description for {category}')
                print(f'Added {category} category.')

    def load_products_from_json(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data = json.load(file)
            for category, products in data['products'].items():
                for product in products:
                    self.create_product(name=product, category=category)
                    print(f'Added {product} to the {category} category.')

    @classmethod
    def __random_price(cls) -> Decimal:
        return Decimal(uniform(cls.MIN_VALUE_FOR_PRICE, cls.MAX_VALUE_FOR_PRICE)).quantize(Decimal('0.01'))

    @classmethod
    def __random_quantity(cls) -> int:
        return randint(cls.MIN_QUANTITY, cls.MAX_QUANTITY)


def main():
    store_filler_admin = StoreFiller(username='admin', password='12345')
    store_filler_admin.load_categories_from_json(filename='data.json')

    store_filler_seller = StoreFiller(username='seller', password='12345')
    store_filler_seller.load_products_from_json(filename='data.json')


if __name__ == '__main__':
    main()
