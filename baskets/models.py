from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Basket(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.PROTECT)
    user = models.OneToOneField(to=User, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s basket | Product: {self.product.name}"
