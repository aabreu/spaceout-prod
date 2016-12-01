# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0013_auto_20161201_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutuser',
            name='personality_insights_input_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_input_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='personality_insights_output_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_output_directory_path, blank=True),
        ),
    ]
