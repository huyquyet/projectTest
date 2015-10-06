# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0003_auto_20150928_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='users',
            field=models.ManyToManyField(related_name='subjects', through='learn.UserSubject', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='users',
            field=models.ManyToManyField(related_name='tasks', through='learn.UserTask', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
