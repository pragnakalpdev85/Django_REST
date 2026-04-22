from django.db import models

class DateTimeStamped(models.Model):
    """
    Abstract base model that provides created_at and updated_at fields.
    Any model that inherits from this will automatically get these fields.
    """
    
    #created_at and updated_at timestamped fields 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Meta informations
    class Meta:
        abstract = True