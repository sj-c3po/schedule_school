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
                ('specific', models.BooleanField(default=False, verbose_name=b'\xd0\xa1\xd0\xbf\xd0\xb5\xd1\x86\xd0\xb8\xd1\x84\xd0\xb8\xd1\x87\xd0\xbd\xd1\x8b\xd0\xb9')),
            ],
            options={
                'db_table': 'cabinet',
                'verbose_name': '\u041a\u0430\u0431\u0438\u043d\u0435\u0442',
                'verbose_name_plural': '\u041a\u0430\u0431\u0438\u043d\u0435\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_max_load', models.IntegerField(default=0, null=True, verbose_name=b'\xd0\x9c\xd0\xb0\xd0\xba\xd1\x81\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb5\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82\xd1\x83', blank=True)),
                ('difficulty_level', models.IntegerField(default=1, verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd1\x81\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbf\xd0\xbe \xd0\xa1\xd0\xb0\xd0\xbd\xd0\x9f\xd0\xb8\xd0\x9d')),
                ('cabinet', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82', to='schedule.Cabinet')),
            ],
            options={
                'ordering': ['subject'],
                'db_table': 'common_rel',
                'verbose_name': '\u0423\u0447\u0435\u0431\u043d\u044b\u0439 \u043f\u043b\u0430\u043d',
                'verbose_name_plural': '\u0423\u0447\u0435\u0431\u043d\u044b\u0439 \u043f\u043b\u0430\u043d',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School_class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parallel', models.IntegerField(verbose_name=b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xb0\xd0\xbb\xd0\xbb\xd0\xb5\xd0\xbb\xd1\x8c')),
                ('letter', models.CharField(max_length=1, null=True, verbose_name=b'\xd0\x91\xd1\x83\xd0\xba\xd0\xb2\xd0\xb0', blank=True)),
                ('class_max_load', models.IntegerField(verbose_name=b'\xd0\x9c\xd0\xb0\xd0\xba\xd1\x81\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb5\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xb0')),
            ],
            options={
                'ordering': ['parallel', 'letter'],
                'db_table': 'school_class',
                'verbose_name': '\u041a\u043b\u0430\u0441\u0441',
                'verbose_name_plural': '\u041a\u043b\u0430\u0441\u0441\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scope', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '\u0421\u0444\u0435\u0440\u0430 \u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u043d\u0438\u044f',
                'verbose_name_plural': '\u0421\u0444\u0435\u0440\u044b \u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u043d\u0438\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_name', models.CharField(max_length=30, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82\xd0\xb0')),
            ],
            options={
                'db_table': 'subject',
                'verbose_name': '\u041f\u0440\u0435\u0434\u043c\u0435\u0442',
                'verbose_name_plural': '\u041f\u0440\u0435\u0434\u043c\u0435\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectTeacherRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teacher_max_load', models.IntegerField(verbose_name=b'\xd0\x9c\xd0\xb0\xd0\xba\xd1\x81\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb5\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82\xd1\x83')),
                ('subject', models.ForeignKey(verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82', to='schedule.Subject')),
            ],
            options={
                'db_table': 'subject_teacher_rel',
                'verbose_name': '\u0423\u0447\u0438\u0442\u0435\u043b\u044c-\u041f\u0440\u0435\u0434\u043c\u0435\u0442',
                'verbose_name_plural': '\u0423\u0447\u0438\u0442\u0435\u043b\u044c-\u041f\u0440\u0435\u0434\u043c\u0435\u0442',
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
                ('staff_type', models.BooleanField(default=False, verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xb2\xd0\xbc\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c')),
                ('class_management', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xbd\xd0\xbe\xd0\xb5 \xd1\x80\xd1\x83\xd0\xba\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe', blank=True, to='schedule.School_class', null=True)),
                ('teacher_cabinet', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xb0\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82', blank=True, to='schedule.Cabinet', null=True)),
            ],
            options={
                'db_table': 'teacher',
                'verbose_name': '\u0423\u0447\u0438\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u0423\u0447\u0438\u0442\u0435\u043b\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subjectteacherrel',
            name='teacher',
            field=models.ForeignKey(verbose_name=b'\xd0\xa3\xd1\x87\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to='schedule.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonrel',
            name='sclass',
            field=models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81', to='schedule.School_class'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonrel',
            name='subject',
            field=models.ForeignKey(verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82', to='schedule.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonrel',
            name='teacher',
            field=models.ForeignKey(verbose_name=b'\xd0\xa3\xd1\x87\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to='schedule.Teacher'),
            preserve_default=True,
        ),
    ]
