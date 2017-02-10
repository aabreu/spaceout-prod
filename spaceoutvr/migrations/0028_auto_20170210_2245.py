# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0027_auto_20170208_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='signin_method',
            field=models.IntegerField(default=0, choices=[(0, b'Email'), (1, b'Facebook'), (2, b'Twitter')]),
        ),
    ]
