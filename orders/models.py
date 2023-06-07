from django.db import models


class Order(models.Model):
    basket = models.ForeignKey(to='baskets.Basket', on_delete=models.PROTECT)
    owner = models.ForeignKey(to='users.Customer', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_detail = models.ForeignKey(to='Payment', on_delete=models.PROTECT, null=True)
    shipping_detail = models.ForeignKey(to='ShippingDetail', on_delete=models.PROTECT, null=True)
    payment_method = models.ForeignKey(to='PaymentMethod', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ID: {self.id} | Owner: {self.owner.username}'


class PaymentDetail(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    card_code = models.CharField(max_length=3)

    def __str__(self):
        return f"Payment detail ID: {self.id}"


class ShippingDetail(models.Model):
    address = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    supplier = models.ForeignKey(to='Supplier', on_delete=models.PROTECT)
    method = models.ForeignKey(to='ShippingMethod', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Shipping detail ID: {self.id}"


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)


class Supplier(models.Model):
    name = models.CharField(max_length=100)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'Failed', 'Failed'

    owner = models.ForeignKey(to='users.Customer', on_delete=models.PROTECT)
    amount = models.IntegerField()
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f'Payment ID: {self.id}'
