from django.urls import re_path
from . import consumers

#all consumers urls
websocket_urlpatterns = [
    re_path(r'^orders/(?P<order_id>[0-9a-fA-F-]+)/$',consumers.OrderConsumer.as_asgi()),
    re_path(r'^restaurants/(?P<restaurant_id>[0-9a-fA-F-]+)/$',consumers.RestaurantConsumer.as_asgi()),
    re_path(r'^customers/(?P<customer_id>[0-9a-fA-F-]+)/$',consumers.CustomerConsumer.as_asgi()),
    re_path(r'^drivers/(?P<driver_id>[0-9a-fA-F-]+)/$',consumers.DriverConsumer.as_asgi()),
]