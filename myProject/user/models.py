from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(_("email"), unique=True, db_index=True)
    is_provider = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    is_active =models.BooleanField(default=False, verbose_name='active')


    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
class Provider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    work_email = models.EmailField(_("work email"),blank=False, unique=True)
    
    

class Seeker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    ed_level = models.CharField(max_length=255, blank=False)



class EmailVerificationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email