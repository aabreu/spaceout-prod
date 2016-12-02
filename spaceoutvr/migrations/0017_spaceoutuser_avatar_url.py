# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0016_spaceoutuser_featured_page_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='avatar_url',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
    ]
