# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0024_auto_20170109_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='facebook_token',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
    ]
