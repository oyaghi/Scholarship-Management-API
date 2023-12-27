from django.contrib import admin
from .models import CustomUser, Provider, Seeker, EmailVerificationToken

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Provider)
admin.site.register(Seeker)
admin.site.register(EmailVerificationToken)





