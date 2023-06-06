from django.db import models

from products.models import Product


class Basket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        FROZEN = 'FROZEN', 'Frozen'
        SUBMITTED = 'SUBMITTED', 'Submitted'

    owner = models.ForeignKey(to='users.Customer', on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id} | {self.owner.username}'s basket"


class BasketLine(models.Model):
    basket = models.ForeignKey(to=Basket, on_delete=models.PROTECT)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['basket', 'product'], name='basket_product')]

    def __str__(self):
        return f"Basket ID: {self.basket.id} | Product ID: {self.product.id} | Quantity: {self.quantity}"
