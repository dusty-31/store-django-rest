from rest_framework import serializers

from users.models import Customer
from products.models import Product

from .models import Basket, BasketLine


class BasketLineSerializer(serializers.ModelSerializer):
    basket = serializers.IntegerField(source='basket.id')
    product = serializers.IntegerField(source='product.id')

    class Meta:
        model = BasketLine
        fields = '__all__'

    def create(self, validated_data):
        basket = Basket.objects.get(pk=validated_data['basket']['id'])
        product = Product.objects.get(pk=validated_data['product']['id'])

        new_basket_line = BasketLine.objects.create(
            basket=basket,
            product=product,
            quantity=validated_data['quantity']
        )
        return new_basket_line

    def update(self, instance, validated_data):
        if validated_data.get('quantity'):
            if validated_data.get('quantity') >= instance.quantity:
                instance.delete()
            else:
                instance.quantity -= validated_data.get('quantity')
                instance.save()
        return instance


class BasketSerializer(serializers.ModelSerializer):
    basket_lines = BasketLineSerializer(many=True, read_only=True, source='basketline_set')
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Basket
        fields = ['id', 'owner', 'status', 'basket_lines']

    def create(self, validated_data):
        owner = Customer.customers.get(username=validated_data['owner']['username'])

        new_basket = Basket.objects.create(
            owner=owner,
            status=Basket.Status.OPEN
        )
        return new_basket

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['basket_lines'] = BasketLineSerializer(instance.basketline_set.all(), many=True).data
        return representation
