# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage
from django.conf import settings
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0005_auto_20161125_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatsonInput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe_id', models.IntegerField()),
                ('chunk_id', models.IntegerField()),
                ('chunk_date_start', models.DateField()),
                ('chunk_date_end', models.DateField()),
                ('data_size', models.FloatField()),
                ('social_network', models.IntegerField(default=0, choices=[(0, b'Facebook'), (1, b'Twitter'), (2, b'Reddit'), (3, b'Sound Cloud')])),
                ('input_url', models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), upload_to=spaceoutvr.models.alchemy_directory_path)),
                ('watson_response_time', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='WatsonOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analysis', models.IntegerField(default=0, choices=[(0, b'Concepts'), (1, b'Keywords'), (2, b'Entities')])),
                ('text', models.CharField(default=b'', max_length=256)),
                ('relevance', models.FloatField()),
                ('watson_input', models.ForeignKey(default=None, to='spaceoutvr.WatsonInput')),
            ],
        ),
        migrations.AlterField(
            model_name='spaceoutcomment',
            name='audio_file',
            field=models.FileField(default=None, storage=spaceoutvr.storage.CommentsStorage(), upload_to=spaceoutvr.models.comment_directory_path),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='fb_location',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='watsoninput',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
