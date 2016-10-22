# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import user_management.api.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('expires', models.DateTimeField(editable=False, default=user_management.api.models.update_expiry)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='authtoken')),
            ],
        ),
    ]
