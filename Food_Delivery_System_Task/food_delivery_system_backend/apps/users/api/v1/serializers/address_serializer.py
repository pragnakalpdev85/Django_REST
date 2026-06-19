from rest_framework import serializers
from apps.users.models import CustomerProfile

class AddressSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, read_only=False) # Used to identify address for updates/deletes
    type = serializers.CharField(max_length=20)
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    zip_code = serializers.CharField(max_length=20)
    is_default = serializers.BooleanField(default=False)


class CustomerAddressSerializer(serializers.ModelSerializer):
    saved_address = AddressSerializer(many=True, default=list)

    class Meta:
        model = CustomerProfile
        fields = ['saved_address']

    def validate_addresses(self, value):
        # Optional: Ensure only one address is set as default
        default_count = sum(1 for addr in value if addr.get('is_default'))
        if default_count > 1:
            raise serializers.ValidationError("Only one address can be set as default.")
        return value   