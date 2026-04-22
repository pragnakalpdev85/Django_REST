from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    User,
    CustomerProfile,
    DriverProfile
)
from apps.restaurants.models import RestaurantProfile
from apps.common.utils.constants import (
    RESTAURANT, CUSTOMER, DRIVER
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create profiles on User creation.
    
    Triggerd by the 'post_save' signal on the User Model. Ensures user profile profile is
    automatically created according to the user role.
    
    Args:
        sender (Model): Model class that sent the signal
        instance (User): instance of the 'User' being saved
        created (bool): true if new record was created else false
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """
    
    if created:
        if instance.role == CUSTOMER:
            CustomerProfile.objects.create(user = instance)
        elif instance.role == RESTAURANT:
            RestaurantProfile.objects.create(owner = instance)
        elif instance.role == DRIVER:
            DriverProfile.objects.create(user = instance)