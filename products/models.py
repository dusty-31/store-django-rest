from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product: {self.name} | Category: {self.category.name}"


class ProductDetail(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.PROTECT)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    resolution = models.CharField(max_length=15, null=True, blank=True)
    processor = models.CharField(max_length=40, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.name} | Category: {self.product.category.name}"
