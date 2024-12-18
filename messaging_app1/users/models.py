# users/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any custom fields if necessary
    pass
