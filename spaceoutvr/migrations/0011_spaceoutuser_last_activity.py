# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0010_spaceoutuser_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='last_activity',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
