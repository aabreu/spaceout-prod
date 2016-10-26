# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spaceoutuser',
            old_name='logitude',
            new_name='longitude',
        ),
    ]
