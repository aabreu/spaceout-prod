# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0008_auto_20161109_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcomment',
            name='audio_file',
            field=models.FileField(default=None, upload_to=spaceoutvr.models.comment_directory_path),
        ),
    ]
