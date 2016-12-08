# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0017_spaceoutuser_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcontent',
            name='type',
            field=models.IntegerField(default=0, choices=[(-1, b'None'), (0, b'Gif'), (1, b'Image'), (2, b'Video')]),
        ),
    ]
