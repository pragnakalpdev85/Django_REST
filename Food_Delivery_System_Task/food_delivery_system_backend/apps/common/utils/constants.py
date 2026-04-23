#users profile's choices
DRIVER = 'delivery_driver'
CUSTOMER = 'customer'
RESTAURANT = 'restaurant_owner'

#Drivers vehicle choices
BIKE = 'bike'
SCOOTER = 'scooter'
CAR = 'car'

#restaurant cuisins choices
ITALIAN = 'italian'
CHINESE = 'chinese'
INDIAN = 'indian'
MEXICAN = 'mexican'
AMERICAN = 'american'
JAPANESE = 'japanese'
THAI = 'thai'
MEDITERRANEAN = 'mediterranean'

#menu item category choices
APPETIZER = 'appetizer'
MAINCOURSE = 'main_course'
DESSERT = 'dessert'
BEVERAGE = 'beverage'
SIDEDISH = 'side_dish'

#dietary information choices
VEGITERIAN = 'vegetarian'
VEGAN = 'vegan'
GLUTENFREE = 'gluten_free'
DAIRYFREE = 'dairy_free'
NONE = 'none'

#order status choices
PENDING = 'pending'
CONFIRMED = 'confirmed'
PREPARING = 'preparing'
READY = 'ready'
PICKEDUP = 'picked_up'
DELIVERED = 'delivered'
CANCELLED = 'cancelled'

#cache timeout values
RESTAURANT_CACHE_TIMEOUT = 5*60
RESTAURANT_PROFILE_CACHE_TIMEOUT = 10*60
MENUITEM_CACHE_TIMEOUT = 15*60
POPULAR_RESTAURANT_CACHE_TIMEOUT = 30*60