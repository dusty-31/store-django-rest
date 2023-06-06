from django.contrib import admin

from .models import Basket, BasketLine


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketLine)
class BasketLineAdmin(admin.ModelAdmin):
    pass
