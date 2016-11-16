# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0012_spaceoutuser_crystal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spaceoutuser',
            old_name='crystal',
            new_name='personality_insights',
        ),
    ]
