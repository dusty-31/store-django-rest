from django.test import TestCase
from requests import Session


class BasketTest(TestCase):
    def setUp(self) -> None:
        self.session = Session()
        self.auth = ('customer', '12345')

    def test_basket_exist(self):
        resp = self.session.get(url='http://127.0.0.1:8000/api/v1/baskets', auth=self.auth).json()
        expected_result = {
            "baskets": [
                {
                    "id": 1,
                    "owner": "customer",
                    "status": "OPEN",
                    "basket_lines": []
                }
            ]
        }
        self.assertDictEqual(resp, expected_result)
