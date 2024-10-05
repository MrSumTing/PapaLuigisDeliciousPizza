from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer, DiscountCode, CustomerPreferences, CustomerData


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

    def create(self, validated_data):
        customer = Customer.objects.get(pk=validated_data.pop('customer'))
        discount_code = DiscountCode.objects.create(**validated_data)
        customer.discount_code = discount_code
        customer.save()
        return discount_code


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPreferences
        fields = '__all__'
        read_only_fields = ('customer',)


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerData
        fields = '__all__'
        read_only_fields = ('customer',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)


class CustomerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True, source='address_line')

    class Meta:
        model = Customer
        fields = [
            'email', 'username', 'password', 'first_name', 'last_name',
            'address', 'postal_code', 'city'
        ]

    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
        }
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


