# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0011_spaceoutuser_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]
