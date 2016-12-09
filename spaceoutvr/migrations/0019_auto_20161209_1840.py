# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0018_auto_20161208_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watsoninput',
            name='recipe_id',
            field=models.IntegerField(choices=[(0, b'Likes'), (1, b'Shares'), (2, b'Posts'), (3, b'Events'), (4, b'Submits'), (5, b'Comments'), (6, b'Upvotes'), (7, b'Saved'), (8, b'Bio'), (9, b'Tweets')]),
        ),
    ]
