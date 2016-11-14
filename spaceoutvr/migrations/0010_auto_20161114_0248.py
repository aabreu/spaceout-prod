# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.models
import spaceoutvr.storage


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0009_auto_20161112_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcomment',
            name='audio_file',
            field=models.FileField(default=None, storage=spaceoutvr.storage.IBMObjectStorage(), upload_to=spaceoutvr.models.comment_directory_path),
        ),
    ]
