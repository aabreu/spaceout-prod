# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0002_auto_20161122_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutuser',
            name='personality_insights',
            field=models.TextField(max_length=2048, null=True),
        ),
    ]
