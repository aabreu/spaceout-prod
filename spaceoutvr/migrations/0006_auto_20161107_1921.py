# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0005_auto_20161107_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutcomment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
