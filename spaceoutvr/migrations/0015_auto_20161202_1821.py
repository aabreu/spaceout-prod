# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.models
import spaceoutvr.storage


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0014_auto_20161202_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutuser',
            name='featured_input_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.featured_directory_path, blank=True),
        ),
    ]
