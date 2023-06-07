from rest_framework import serializers

from .models import Order, PaymentDetail, ShippingDetail, PaymentMethod, Payment
from .services import get_total_amount

from baskets.models import Basket
from users.models import Customer


class OrderSerializer(serializers.ModelSerializer):
    basket = serializers.IntegerField(source='basket.id')
    owner = serializers.IntegerField(source='owner.id')
    total_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        basket = Basket.objects.get(pk=validated_data['basket']['id'])
        owner = Customer.customers.get(pk=validated_data['owner']['id'])
        total_amount = get_total_amount(basket=basket)

        new_order = Order.objects.create(
            basket=basket,
            owner=owner,
            total_amount=total_amount,
        )
        return new_order


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = '__all__'


class ShippingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetail
        fields = ['__all__']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['__all__']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['__all__']
