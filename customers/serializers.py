from rest_framework import serializers
from .models import Customer
import re

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'mobile', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        # Check if email already exists (for creation)
        if Customer.objects.filter(email=value).exists():
            # For updates, allow same email
            if self.instance and self.instance.email == value:
                return value
            raise serializers.ValidationError("Customer with this email already exists.")
        return value

    def validate_mobile(self, value):
        clean_mobile = re.sub(r'[^\d+]', '', value)
        
        if not re.match(r'^\+?1?\d{10,13}$', clean_mobile):
            raise serializers.ValidationError(
                "Mobile number must be 10-13 digits, optionally starting with '+' and country code."
            )
        return value

    def validate(self, attrs):
        return attrs


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'mobile', 'created_at']