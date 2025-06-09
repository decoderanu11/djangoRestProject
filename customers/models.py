import uuid
from django.db import models
from django.core.validators import RegexValidator

class Customer(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  
        editable=False       # Can't be changed via forms/admin
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Custom validator for mobile
    mobile = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{10,13}$',
                message="Mobile number must be entered in the format: '+999999999'. Up to 13 digits allowed."
            )
        ]
    )
    
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated on every save
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        
    def __str__(self):
        return f"{self.name} - {self.email}"