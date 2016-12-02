# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spaceoutvr.storage


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0013_auto_20161201_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceoutuser',
            name='featured_input_url',
            field=models.FileField(default=None, storage=spaceoutvr.storage.WatsonStorage(), null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='watsoninput',
            name='recipe_id',
            field=models.IntegerField(choices=[(0, b'Likes'), (1, b'Shares'), (2, b'Posts'), (3, b'Events'), (4, b'Submits'), (5, b'Comments'), (6, b'Upvotes'), (7, b'Saved'), (8, b'Bio')]),
        ),
    ]
