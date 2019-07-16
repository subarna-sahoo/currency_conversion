
from django.db import models

class Currency(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    name = models.CharField(max_length=20, help_text='Enter Currency Pair')
    symbol = models.CharField(max_length=20, help_text='Enter Currency Pair')

    # Metadata
    class Meta: 
        ordering = ['-name']
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
