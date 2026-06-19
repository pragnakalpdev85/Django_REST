from .customer_profile import CustomerProfileSerializer
from .driver_profile import DriverProfileSerializer
from .driver_info import DriverInfoSerializer
from .user import RegisterSerializer
from .address_serializer import CustomerAddressSerializer, AddressSerializer

__all__ = [
    'CustomerProfileSerializer',
    'DriverProfileSerializer',
    'RegisterSerializer',
    'DriverInfoSerializer',
    'UserInfoSerializer',
    'CustomerAddressSerializer',
    'AddressSerializer'
]