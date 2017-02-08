# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0026_auto_20170206_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='play_intro',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='user_name_for_voice',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
