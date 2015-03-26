# -*- coding: utf-8 -*-

from django.db import models

# class Administration(models.Model):
#     class Meta():
#         db_table = 'admin'
#     login = models.CharField(max_length=15)
#     password = models.CharField(max_length=20)


class School_class(models.Model):
    class Meta():
        db_table = 'school_class'

    class_name = models.CharField(max_length=10) # 11а и хватит (юникод?)
    class_max_load = models.IntegerField()

class Cabinet(models.Model):
    class Meta():
        db_table = 'cabinet'

    cabinet_number = models.CharField(max_length=10)  # char - а вдруг там буквы?


class Subject(models.Model):
    class Meta():
        db_table = 'subject'

    subject_name = models.CharField(max_length=30)
    sclass = models.ForeignKey('School_class')
    subject_cabinet = models.ForeignKey('Cabinet')
    subject_max_load = models.IntegerField()            # максимальная нагрузка на конкретный класс

class Teacher(models.Model):
    class Meta():
        db_table = 'teacher'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    teacher_subject = models.ForeignKey('Subject')
    class_management = models.ForeignKey('School_class')
    teacher_cabinet = models.ForeignKey('Cabinet')
    teacher_max_load = models.IntegerField()                # максимальная нагрузка по указанному предмету