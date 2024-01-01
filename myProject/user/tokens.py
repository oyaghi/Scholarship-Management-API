from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from .models import CustomUser


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, data, timestamp):
        user = CustomUser.objects.get(email=data.email)
        return (
            force_str(user.pk) +
            force_str(timestamp) +
            force_str(user.is_active) +
            force_str(user.email)  # Add user email for uniqueness
        )




class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, data, timestamp):
        user = CustomUser.objects.get(email=data.email)
        return (
            force_str(user.pk) +
            force_str(timestamp) +
            force_str(user.is_active) +
            force_str(user.email)  # Add user email for uniqueness
        )

