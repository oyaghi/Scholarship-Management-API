from django.contrib import admin
from .models import CustomUser, Provider, Seeker
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Provider)
admin.site.register(Seeker)





