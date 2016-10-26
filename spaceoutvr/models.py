from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser

class SpaceoutUser(EmailAbstractUser):
    # Required
    objects = EmailUserManager()
