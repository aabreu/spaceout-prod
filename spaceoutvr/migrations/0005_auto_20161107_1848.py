# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0004_spaceoutroom_definition'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SpaceoutMessage',
            new_name='SpaceoutComment',
        ),
    ]
