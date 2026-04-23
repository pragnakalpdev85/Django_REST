from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from apps.common.models import DateTimeStamped, UUIDModel, AVGRating
from apps.common.utils.constants import (
    PENDING, CONFIRMED, PREPARING, READY, PICKEDUP,
    DELIVERED, CANCELLED
)

# Create your models here.
class Order(UUIDModel, DateTimeStamped):
    """
    Order model provides fields restaurant, customer, driver, order_number,
    status, delivery_address, subtotal, delivery_fee, tax, total_amount,
    special_instructions, estimated_delivery_time, actual_delivery_time.    
    """
    
    #status choices
    STATUS = (
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (PREPARING, 'Preparing'),
        (READY, 'Ready'),
        (PICKEDUP, 'Picked Up'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    )
    
    #entities related with order 
    restaurant = models.ForeignKey(
        'restaurants.RestaurantProfile', 
        on_delete=models.CASCADE, 
        related_name='restaurant_order'
    )
    customer = models.ForeignKey(
        'users.CustomerProfile', 
        on_delete=models.CASCADE, 
        related_name='customer_order'
    )
    driver = models.ForeignKey(
        'users.DriverProfile', 
        on_delete=models.CASCADE, 
        related_name='driver_order',
        null=True,
        blank=True
    )
    
    #order basic details
    order_number = models.IntegerField(unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS, default=PENDING)
    special_instructions = models.TextField(null=True, blank=True)
    delivery_address = models.TextField()
    
    #order value
    subtotal = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    delivery_fee = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    tax = models.DecimalField(default=0.08, decimal_places=2, max_digits=8)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    
    #order time stamps
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    
    # order confirmation time and delivery time
    confirmed_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    actual_delivery_time = models.DateTimeField(blank=True, null=True)
        
    #Meta informations
    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_order_idx'),
            models.Index(fields=['restaurant'], name='restaurant_order_idx'),
            models.Index(fields=['customer'], name='customer_idx'),
            models.Index(fields=['driver'], name='driver_idx'),
            models.Index(fields=['status'], name='status_idx'),
            models.Index(fields=['customer', 'status'], name='order_customer_status_idx'),
            models.Index(fields=['driver', 'status'], name='order_driver_status_idx'),
        ]
        
    def save(self, *args, **kwargs):
        """save method is overrided to generate order number"""
        last = Order.objects.all().order_by('order_number').last()
        if last:
            self.order_number = last.order_number + 1
        else:
            self.order_number = 1
            
        return super().save(*args, **kwargs)
    
    # additional methods
    def calculate_total(self):
        """calculates total amount of the order"""
        subtotal = sum(
            item.price * item.quantity for item in self.order_menu.all()
        )
        self.subtotal = float(subtotal)
        self.total_amount = (float(subtotal) * float(self.tax)) + float(subtotal) + float(self.delivery_fee)
        return self.total_amount
    
    def can_cancel(self):
        """user can cancel the order or not"""
        return self.status in (PENDING, CONFIRMED, PREPARING)
        
    def is_delivered(self):
        """checks weather the order is delivered or not"""
        return self.status == DELIVERED
    
    def calculate_estimated_time(self):
        """Calculates estimated time"""
        self.estimated_delivery_time = sum(
            item.quantity * item.menu_item.preparation_time for item in self.order_menu.all()
        )
        self.estimated_delivery_time = timezone.now() + timedelta(minutes=self.estimated_delivery_time)
        return self.estimated_delivery_time
    
      
class Cart(UUIDModel, DateTimeStamped):
    """
    Cart model provides fields subtotal, delivery_fee, tax, total_amount. 
    """
    customer = models.ForeignKey(
        'users.CustomerProfile', 
        on_delete=models.CASCADE, 
        related_name='customer_cart'
    )
    #order value
    subtotal = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    delivery_fee = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    tax = models.DecimalField(default=0.08, decimal_places=2, max_digits=8)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    
    #meta informations
    class Meta:
        db_table = 'carts'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_cart_idx'),
        ]
        
    def calculate_total(self):
        """calculates total amount of the order"""
        subtotal = sum(
            item.price * item.quantity for item in self.cart_menu.all()
        )
        self.subtotal = float(subtotal)
        self.total_amount = (float(subtotal) * float(self.tax)) + float(subtotal) + float(self.delivery_fee)
        return self.total_amount
    
        
class OrderItem(UUIDModel, DateTimeStamped):
    """
    OrderItem model provides fields order, menu_item, quantity, price, special_instrutions
    Model represents Items included in perticular order
    """
    
    #foriegnkey to order
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='order_menu',
        null=True,
        blank=True
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_menu',
        null=True,
        blank=True
    )
    
    #foriegnkey to menu_item
    menu_item = models.ForeignKey(
        'restaurants.MenuItem',
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    
    #basic fields
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    special_instructions = models.TextField(null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    
    #Meta informations
    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_order_item_idx'),
            models.Index(fields=['menu_item'], name='menu_item_idx'),
            models.Index(fields=['order'], name='order_idx')
        ]
    
    def save(self, *args, **kwargs):
        "Assigns price value from menuitems price"
        self.price = self.menu_item.price
        self.total = self.calculate_total()
        return super().save(*args, **kwargs)
        
    def calculate_total(self):
        """calculates total of order item"""
        self.total = (self.price * self.quantity)
        return self.total