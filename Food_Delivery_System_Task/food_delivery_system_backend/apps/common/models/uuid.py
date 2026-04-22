import uuid
from django.db import models

class UUIDModel(models.Model):
    """
    Abstract model that uses UUID instead of auto-incrementing integer ID.
    Useful for security (can't guess IDs) and distributed systems.
    """
    # Use UUID as primary key instead of auto-incrementing integer
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True