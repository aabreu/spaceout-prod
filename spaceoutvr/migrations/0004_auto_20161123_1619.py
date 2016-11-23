# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0003_auto_20161122_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcontent',
            name='url',
            field=models.CharField(max_length=2048),
        ),
    ]
