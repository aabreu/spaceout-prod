# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0003_auto_20161103_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutroom',
            name='definition',
            field=models.ForeignKey(default=None, to='spaceoutvr.SpaceoutRoomDefinition'),
        ),
    ]
