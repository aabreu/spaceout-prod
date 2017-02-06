# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0025_auto_20170126_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='twitter_token',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
    ]
