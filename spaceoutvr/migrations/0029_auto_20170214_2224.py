# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0028_auto_20170210_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcontent',
            name='source',
            field=models.IntegerField(default=0, choices=[(0, b'Giphy'), (1, b'Wiki'), (2, b'Youtube'), (3, b'Google Images'), (4, b'Profile Image')]),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='play_intro',
            field=models.BooleanField(default=False),
        ),
    ]
