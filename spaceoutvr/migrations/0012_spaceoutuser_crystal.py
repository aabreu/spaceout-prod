# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0011_spaceoutcontent_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='crystal',
            field=models.TextField(default=b''),
        ),
    ]
