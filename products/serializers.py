from rest_framework import serializers

from users.models import Seller

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        category = Category.objects.get(name=validated_data['category']['name'])
        owner = Seller.sellers.get(username=validated_data['owner']['username'])

        new_product = Product.objects.create(
            name=validated_data['name'],
            category=category,
            price=validated_data['price'],
            quantity=validated_data['quantity'],
            owner=owner
        )
        return new_product

    def update(self, instance, validated_data):
        category = Category.objects.get(name=validated_data['category']['name'])

        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get(category, instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than zero.')
        return value
