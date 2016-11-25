# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0004_auto_20161123_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='fb_birthdate',
            field=models.CharField(default=b'', max_length=16),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='fb_gender',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='fb_location',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
