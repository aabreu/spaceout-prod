# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0007_auto_20161108_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutcomment',
            name='audio_file',
            field=models.FileField(default=None, upload_to=b'comments/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='spaceoutcontent',
            name='source',
            field=models.IntegerField(default=0, choices=[(0, b'Giphy'), (1, b'Wiki'), (2, b'Youtube'), (3, b'Google Images')]),
        ),
    ]
