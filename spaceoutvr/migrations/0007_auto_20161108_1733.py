# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
# from authemail.models import EmailUserManager
from spaceoutvr.models import SpaceoutUser

def create_super_user(apps, schena_editor):
    SpaceoutUser.objects.create_superuser('aa@spaceoutvr.com', 'Daydr3am10')

def create_room_definitions(apps, schena_editor):
    SpaceoutRoomDefinition = apps.get_model("spaceoutvr", "SpaceoutRoomDefinition")
    room_definition = SpaceoutRoomDefinition()
    room_definition.type = 0
    room_definition.capacity = 14
    room_definition.save()

class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0006_auto_20161107_1921'),
    ]

    operations = [
        migrations.RunPython(create_super_user),
        migrations.RunPython(create_room_definitions),
    ]
