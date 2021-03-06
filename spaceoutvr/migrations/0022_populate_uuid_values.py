# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def gen_username(apps, schema_editor):
    k = 0
    MyModel = apps.get_model('spaceoutvr', 'SpaceoutUser')
    for row in MyModel.objects.all():
        row.user_name = "spaceout_user_%s" % k
        row.save()
        k = k + 1

class Migration(migrations.Migration):

    dependencies = [
        ('spaceoutvr', '0021_spaceoutuser_spaceout_name'),
    ]

    operations = [
        migrations.RunPython(gen_username, reverse_code=migrations.RunPython.noop),
    ]
