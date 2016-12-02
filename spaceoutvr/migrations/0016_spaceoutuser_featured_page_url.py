# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0015_auto_20161202_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='featured_page_url',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
    ]
