# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_auto_20150928_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
