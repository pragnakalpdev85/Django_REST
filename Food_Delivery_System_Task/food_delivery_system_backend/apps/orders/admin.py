from django.contrib import admin
from .models import Order, Cart, OrderItem

# Register your models here.
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(OrderItem)
