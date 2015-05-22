# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0018_auto_20150522_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='cabinet_number',
            field=models.CharField(max_length=10, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xba\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82\xd0\xb0'),
        ),
    ]
