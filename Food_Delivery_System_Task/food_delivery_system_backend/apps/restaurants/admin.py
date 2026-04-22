from django.contrib import admin
from .models import RestaurantProfile, MenuItem, Review

admin.site.register(RestaurantProfile)
admin.site.register(MenuItem)
admin.site.register(Review)
