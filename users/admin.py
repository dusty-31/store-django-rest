from django.contrib import admin

from .models import User, Customer, Seller


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass
