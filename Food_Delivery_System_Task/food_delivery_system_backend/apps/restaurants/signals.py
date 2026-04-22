from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


@receiver([post_save, post_delete], sender='restaurants.Review')
def update_rating_on_review(sender, instance, **kwargs):
    """
    Signal handler to automatically update average rating in menu items and restaurant
    
    Triggerd by the 'post_save' and 'post_delete' signals on the review model, and updates average rating
    of the menu item or restaurant
    
    Args:
        sender (Model): Model class that sent the signal
        instance (Review): instance of the 'Review' being saved/deleted
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """

    if instance.restaurant:
        instance.restaurant.update_averge_rating()
    
    if instance.menu_item:
        instance.menu_item.update_averge_rating()

        
@receiver([post_save, post_delete], sender='restaurants.MenuItem')
def invalidate_menu_item_cache(sender, instance, **kwargs):
    """
    Signal handler to automatically delete cache of menu items.
    Triggerd by the 'post_save' or 'post_delete' signal on the menu_item model.
    
    Args:
        sender (Model): Model class that sent the signal
        instance (Review): instance of the 'MenuItem' being saved
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """
    
    cache.delete(f"restaurant_menu_{instance.restaurant.id}")
    cache.delete("restaurant_popular")

    
@receiver([post_save], sender='restaurants.Review')
def invalidate_restaurant_cache(sender, instance, **kwargs):
    """
    Signal handler to automatically delete cache of restaurant.
    Triggerd by the 'post_save' signal on the review model.
    
    Args:
        sender (Model): Model class that sent the signal
        instance (Review): instance of the 'Review' being saved
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """
    if instance.restaurant:
        cache.delete(f"restaurant_detail_{instance.restaurant.id}")
        cache.delete("restaurant_popular")
    
    
    