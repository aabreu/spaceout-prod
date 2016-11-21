# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0013_auto_20161115_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceoutNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Comment')])),
                ('comment', models.ForeignKey(to='spaceoutvr.SpaceoutComment')),
            ],
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='notifications',
            field=models.ManyToManyField(to='spaceoutvr.SpaceoutNotification'),
        ),
    ]
