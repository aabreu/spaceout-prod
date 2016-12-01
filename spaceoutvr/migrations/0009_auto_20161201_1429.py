# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0008_auto_20161130_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='personality_insights',
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='personality_insights_input_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_input_directory_path),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='personality_insights_output_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_output_directory_path),
        ),
    ]
