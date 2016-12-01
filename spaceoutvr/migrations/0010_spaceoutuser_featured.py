# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0009_auto_20161201_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
