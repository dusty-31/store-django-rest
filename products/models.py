from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import Seller


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(to=Seller, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"ID : {self.id} | Product: {self.name} | Category: {str(self.category)} | Price: {self.price} $"


@receiver(signal=pre_delete, sender=Seller)
def set_product_inactive(sender, instance, **kwargs):
    instance.is_active = False


class ProductDetail(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.PROTECT)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    resolution = models.CharField(max_length=15, null=True, blank=True)
    processor = models.CharField(max_length=40, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Product detail'

    def __str__(self):
        return str(self.product)
