# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage
from django.conf import settings
import django.utils.timezone
import spaceoutvr.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceoutUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user has completed the email verification process to allow login.', verbose_name='verified')),
                ('phone_number', models.CharField(default=b'', max_length=30)),
                ('latitude', models.CharField(default=b'', max_length=30)),
                ('longitude', models.CharField(default=b'', max_length=30)),
                ('personality_insights', models.TextField(default=b'')),
                ('notification_id', models.CharField(default=b'', max_length=256)),
                ('facebook_id', models.CharField(default=b'', max_length=128)),
                ('reddit_id', models.CharField(default=b'', max_length=128)),
                ('twitter_id', models.CharField(default=b'', max_length=128)),
                ('soundcloud_id', models.CharField(default=b'', max_length=128)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='SpaceoutComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('audio_file', models.FileField(default=None, storage=spaceoutvr.storage.IBMObjectStorage(), upload_to=spaceoutvr.models.comment_directory_path)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceoutContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Gif'), (1, b'Image'), (2, b'Video')])),
                ('idx', models.IntegerField(default=0)),
                ('source', models.IntegerField(default=0, choices=[(0, b'Giphy'), (1, b'Wiki'), (2, b'Youtube'), (3, b'Google Images')])),
                ('query', models.CharField(max_length=256)),
                ('weight', models.FloatField(default=0)),
                ('url', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceoutNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Comment')])),
                ('read', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(to='spaceoutvr.SpaceoutComment')),
                ('user', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceoutRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
        migrations.AddField(
            model_name='spaceoutroom',
            name='definition',
            field=models.ForeignKey(default=None, to='spaceoutvr.SpaceoutRoomDefinition'),
        ),
        migrations.AddField(
            model_name='spaceoutroom',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spaceoutcontent',
            name='room',
            field=models.ForeignKey(to='spaceoutvr.SpaceoutRoom'),
        ),
        migrations.AddField(
            model_name='spaceoutcomment',
            name='content',
            field=models.ForeignKey(to='spaceoutvr.SpaceoutContent'),
        ),
    ]
