from rest_framework import serializers

from .models import User, Seller, Customer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        if validated_data['role'] == User.Role.SELLER.name:
            new_user = Seller.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
            )
        elif validated_data['role'] == User.Role.CUSTOMER.name:
            new_user = Customer.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
            )
        else:
            return None

        new_user.save()
        return new_user
