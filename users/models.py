from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

from baskets.models import Basket


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
        SELLER = 'SELLER', 'Seller'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def __str__(self):
        return f'{self.role} - {self.username}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER
    customers = CustomerManager()

    class Meta:
        proxy = True


class CustomerProfile(models.Model):
    user = models.OneToOneField(to=Customer, on_delete=models.CASCADE)
    customer_id = models.IntegerField(null=True, blank=True)


@receiver(signal=post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'CUSTOMER':
        CustomerProfile.objects.create(user=instance)


@receiver(signal=post_save, sender=Customer)
def create_basket(sender, instance, created, **kwargs):
    if created and instance.role == 'CUSTOMER':
        Basket.objects.create(owner=instance)


class SellerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SELLER)


class Seller(User):
    base_role = User.Role.SELLER
    sellers = SellerManager()

    class Meta:
        proxy = True


class SellerProfile(models.Model):
    user = models.OneToOneField(to=Seller, on_delete=models.CASCADE)
    seller_id = models.IntegerField(null=True, blank=True)


@receiver(signal=post_save, sender=Seller)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'SELLER':
        SellerProfile.objects.create(user=instance)
