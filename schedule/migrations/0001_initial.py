# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cabinet_number', models.CharField(max_length=10, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xba\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82\xd0\xb0')),
            ],
            options={
                'db_table': 'cabinet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School_class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.CharField(max_length=10, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xb0')),
                ('class_max_load', models.IntegerField(verbose_name=b'\xd0\x9c\xd0\xb0\xd0\xba\xd1\x81\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb5\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xb0')),
            ],
            options={
                'db_table': 'school_class',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_name', models.CharField(max_length=30, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82\xd0\xb0')),
                ('subject_max_load', models.IntegerField(verbose_name=b'\xd0\x9c\xd0\xb0\xd0\xba\xd1\x81\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb5\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd1\x83')),
                ('sclass', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81', to='schedule.School_class')),
                ('subject_cabinet', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82', to='schedule.Cabinet')),
            ],
            options={
                'db_table': 'subject',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=50, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x8f')),
                ('first_name', models.CharField(max_length=50, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('middle_name', models.CharField(max_length=50, verbose_name=b'\xd0\x9e\xd1\x82\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe')),
                ('class_management', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xbd\xd0\xbe\xd0\xb5 \xd1\x80\xd1\x83\xd0\xba\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe', to='schedule.School_class')),
                ('teacher_cabinet', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82', to='schedule.Cabinet')),
                ('teacher_subject', models.ForeignKey(to='schedule.Subject')),
            ],
            options={
                'db_table': 'teacher',
            },
            bases=(models.Model,),
        ),
    ]
