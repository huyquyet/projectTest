# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0004_auto_20150928_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='status',
            field=models.BooleanField(default=False, help_text=b'Activity'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='subject_id',
            field=models.ForeignKey(related_name='task', to='learn.Subject'),
        ),
    ]
