# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0006_auto_20161129_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatsonBlacklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(default=b'', max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='watsoninput',
            name='recipe_id',
            field=models.IntegerField(choices=[(0, b'Likes'), (1, b'Shares'), (2, b'Posts'), (3, b'Events')]),
        ),
    ]
