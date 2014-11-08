# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CCD', '0004_auto_20141107_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patients', models.ManyToManyField(to='CCD.Patient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
