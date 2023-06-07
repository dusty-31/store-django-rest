from django.contrib import admin

from .models import Order, PaymentMethod


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethod)
class Payment(admin.ModelAdmin):
    pass
