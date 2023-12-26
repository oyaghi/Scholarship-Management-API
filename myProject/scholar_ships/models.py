from django.db import models
from user.models import Provider, Seeker
from django.core.exceptions import ValidationError


# Create your models here.


    
def validate_image_size(value):
    limit = 3 * 1024 * 1024  # 3MB limit
    if value.size > limit:
        raise ValidationError(f"Image file size too large (maximum is 3MB).")


class Scholarship(models.Model):
    
    provider        = models.ForeignKey(Provider, on_delete=models.CASCADE)
    seeker          = models.ManyToManyField(Seeker, through="Scholarship_Seeker")
    category        = models.CharField(db_index=True) # is it possible to add indexing to filed that isn't unique
    description     = models.TextField()
    scholar_link    = models.URLField(max_length=255) # how to deal with links 
    start_date      = models.DateField()  # Change the start date  to just date dd/MM/YY
    end_date        = models.DateField()  # Change the end date  to just date dd/MM/YY
    name            = models.CharField(max_length=255)
    status          = models.BooleanField(default=False)  # Checking if the scholar is checked or not 
    created_at      = models.DateTimeField(auto_now_add=True)
    image           = models.ImageField(upload_to='images/',validators=[validate_image_size])
    



class Scholarship_Seeker(models.Model):
    
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  

    