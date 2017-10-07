# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bdate', models.DateField()),
                ('bcontent', models.CharField(max_length=10)),
                ('bcomment', models.CharField(max_length=50)),
                ('bmoney', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_delete', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'bill',
            },
        ),
    ]
