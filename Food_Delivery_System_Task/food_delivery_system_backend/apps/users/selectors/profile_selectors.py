from apps.users.models import CustomerProfile, DriverProfile
from apps.restaurants.models import Review

class ProfileSelectors:
    """
    Profile selector manages different queries for driver and customer 
    profile models.
    """
    
    @staticmethod
    def get_customer_profile_queryset():
        """
        Returns query for customer profile viewset
        """
        return ( 
            CustomerProfile.objects.all()
            .select_related('user') 
        )
    
    @staticmethod
    def get_driver_profile_queryset():
        """
        Returns query for driver profile viewset
        """
        return (
            DriverProfile.objects.all()
            .select_related('user')
            .prefetch_related('driver_review')
        )
    
    @staticmethod 
    def get_active_drivers_queryset():
        """
        Returns query for filtering driver from their activity status
        """
        return (
            DriverProfile.objects
            .filter(is_available=True)
            .all()
        )
        
    @staticmethod
    def filter_driver_profile_by_user(driver):
        """
        Returns driver profile from user with delivery driver role
        """
        
        return (
            DriverProfile.objects
            .filter(user=driver)
            .first()
        )
        
    @staticmethod
    def filter_customer_profile_by_user(customer):
        """
        Returns customer profile from user with customer role
        """
        
        return (
            CustomerProfile.objects
            .filter(user=customer)
            .first()
        )
        
        
    @staticmethod
    def get_reviews_of_driver(driver):
        """
        Returns reviews of driver
        """
        
        return (
            Review.objects
            .select_related('driver')
            .filter(driver = driver)
        )
        