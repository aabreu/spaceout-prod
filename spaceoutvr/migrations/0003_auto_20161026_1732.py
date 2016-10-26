# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0002_auto_20161026_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceoutProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=30)),
                ('latitude', models.CharField(default=b'', max_length=30)),
                ('longitude', models.CharField(default=b'', max_length=30)),
                ('notification_id', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='notification_id',
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='spaceoutprofile',
            name='user',
            field=models.OneToOneField(related_name='profile_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
