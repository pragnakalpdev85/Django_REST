from django.db import models
from django.db.models import Avg

class AVGRating(models.Model):
    """
    Abstract base model that provides average_rating field and method to calculate field.
    Any model that inherits from this will automatically get these fields.
    """
    
    average_rating = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    total_reviews = models.IntegerField(default=0)
    
    #Meta informations
    class Meta:
        abstract = True
        
    def update_averge_rating(self, review_queryset):
        """Updates average rating of the restaurant"""
        
        #gets reviews of perticular restaurant
        result = review_queryset.aggregate(average=Avg('rating'))
        self.average_rating = result['average']
        self.total_reviews = review_queryset.count()
        self.save(update_fields=['average_rating', 'total_reviews', 'updated_at'])