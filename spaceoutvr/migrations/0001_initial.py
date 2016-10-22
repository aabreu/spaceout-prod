# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import user_management.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceoutUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('email_verified', models.BooleanField(default=False, help_text='Indicates if the email address has been verified.', verbose_name='Email verified?')),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', blank=True, verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', to='auth.Permission', blank=True, verbose_name='user permissions', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
            bases=(user_management.models.mixins.EmailVerifyUserMethodsMixin, user_management.models.mixins.NameUserMethodsMixin, models.Model),
        ),
    ]
