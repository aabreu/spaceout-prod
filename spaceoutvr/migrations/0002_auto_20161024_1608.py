# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spaceoutuser',
            options={'verbose_name_plural': 'users', 'verbose_name': 'user'},
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='email_verified',
        ),
        migrations.RemoveField(
            model_name='spaceoutuser',
            name='name',
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='first_name',
            field=models.CharField(blank=True, verbose_name='first name', max_length=30),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='is_verified',
            field=models.BooleanField(help_text='Designates whether this user has completed the email verification process to allow login.', default=False, verbose_name='verified'),
        ),
        migrations.AddField(
            model_name='spaceoutuser',
            name='last_name',
            field=models.CharField(blank=True, verbose_name='last name', max_length=30),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='email',
            field=models.EmailField(unique=True, verbose_name='email address', max_length=255),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='is_active',
            field=models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='spaceoutuser',
            name='is_staff',
            field=models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status'),
        ),
    ]
