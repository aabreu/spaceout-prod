# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0020_auto_20161221_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='user_name',
            field=models.CharField(default="", null=True, max_length=30),
        ),
    ]
