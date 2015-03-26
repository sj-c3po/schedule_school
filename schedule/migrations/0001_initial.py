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
                ('cabinet_number', models.CharField(max_length=10)),
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
                ('class_name', models.CharField(max_length=10)),
                ('class_max_load', models.IntegerField()),
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
                ('subject_name', models.CharField(max_length=30)),
                ('subject_max_load', models.IntegerField()),
                ('sclass', models.ForeignKey(to='schedule.School_class')),
                ('subject_cabinet', models.ForeignKey(to='schedule.Cabinet')),
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
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('teacher_max_load', models.IntegerField()),
                ('class_management', models.ForeignKey(to='schedule.School_class')),
                ('teacher_cabinet', models.ForeignKey(to='schedule.Cabinet')),
                ('teacher_subject', models.ForeignKey(to='schedule.Subject')),
            ],
            options={
                'db_table': 'teacher',
            },
            bases=(models.Model,),
        ),
    ]
