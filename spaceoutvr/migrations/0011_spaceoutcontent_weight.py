# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0010_auto_20161114_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutcontent',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
