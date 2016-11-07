# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0002_spaceoutroom_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceoutMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('author', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('content', models.ForeignKey(to='spaceoutvr.SpaceoutContent')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceoutRoomDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Home'), (1, b'360 Theatre')])),
                ('capacity', models.IntegerField(default=14)),
            ],
        ),
        migrations.RemoveField(
            model_name='spaceoutroom',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='spaceoutroom',
            name='type',
        ),
    ]
