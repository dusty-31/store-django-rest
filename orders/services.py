from decimal import Decimal

from baskets.models import Basket, BasketLine


def get_total_amount(basket: Basket):
    basket_lines = list(BasketLine.objects.filter(basket=basket))
    total_amount = 0
    for basket_line in basket_lines:
        total_amount += basket_line.product.price * basket_line.quantity
    return Decimal(total_amount)
