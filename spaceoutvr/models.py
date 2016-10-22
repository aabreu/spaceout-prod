from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user_management.models.mixins import VerifyEmailMixin


class SpaceoutUser(VerifyEmailMixin, PermissionsMixin, AbstractBaseUser):
    pass
