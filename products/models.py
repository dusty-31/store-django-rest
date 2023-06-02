from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(to='self', on_delete=models.PROTECT, null=True)
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
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(to='users.Seller', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"ID : {self.id} | Product: {self.name} | Category: {str(self.category)} | Price: {self.price} $"


class ProductDetail(models.Model):
    # category = models.OneToOneField(to=Category, on_delete=models.PROTECT)
    product = models.OneToOneField(to=Product, on_delete=models.PROTECT)
    description = models.TextField()
    # quantity = models.PositiveIntegerField(default=0)
    resolution = models.CharField(max_length=15, null=True, blank=True)
    processor = models.CharField(max_length=40, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Product detail'

    def __str__(self):
        return str(self.product)
