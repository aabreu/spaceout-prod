# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0012_spaceoutuser_popularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceoutuser',
            name='facebook_id',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='fb_birthdate',
            field=models.CharField(default=b'', max_length=16, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='fb_gender',
            field=models.CharField(default=b'', max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='fb_location',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='latitude',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='longitude',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='notification_id',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='personality_insights_input_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_input_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='personality_insights_output_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=spaceoutvr.models.personality_insights_output_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='phone_number',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='reddit_id',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='soundcloud_id',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='twitter_id',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
    ]
