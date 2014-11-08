# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CCD', '0003_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='chart',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]
