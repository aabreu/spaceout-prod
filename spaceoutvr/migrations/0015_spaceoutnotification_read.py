# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0014_auto_20161119_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutnotification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
