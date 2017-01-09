# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
# from authemail.models import EmailUserManager
from spaceoutvr.models import SpaceoutUser

def create_super_user(apps, schena_editor):
    try:
        superuser = SpaceoutUser.objects.get(is_staff=True)
    except:
        SpaceoutUser.objects.create_superuser('aa@spaceoutvr.com', 'Daydr3am10', user_name='spaceoutvr')


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0023_remove_uuid_null'),
    ]

    operations = [
        migrations.RunPython(create_super_user),
    ]
