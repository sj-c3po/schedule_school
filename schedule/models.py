# -*- coding: utf-8 -*-

from django.db import models

class School_class(models.Model):
    class Meta():
        db_table = 'school_class'

    id = models.AutoField(primary_key=True)
    class_name = models.CharField('Название класса', max_length=10) # 11а и хватит (юникод?)
    class_max_load = models.IntegerField('Максимальная недельная нагрузка класса')

    def __str__(self):
        return self.class_name


class Cabinet(models.Model):
    class Meta():
        db_table = 'cabinet'

    id = models.AutoField(primary_key=True)
    cabinet_number = models.CharField('Номер кабинета', max_length=10)  # char - а вдруг там буквы?

    def __str__(self):
        return self.cabinet_number


class Subject(models.Model):
    class Meta():
        db_table = 'subject'

    id = models.AutoField(primary_key=True)
    subject_name = models.CharField('Название предмета', max_length=30)
    sclass = models.ForeignKey('School_class', verbose_name = 'Класс')
    subject_cabinet = models.ForeignKey('Cabinet', verbose_name = 'Кабинет')
    subject_max_load = models.IntegerField('Максимальная недельная нагрузка по классу')            # максимальная нагрузка на конкретный класс

    def __str__(self):
        return self.subject_name


class Teacher(models.Model):
    class Meta():
        db_table = 'teacher'

    id = models.AutoField(primary_key=True)
    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    middle_name = models.CharField('Отчество', max_length=50)
    teacher_subject = models.ForeignKey('Subject', verbose_name = 'Предмет')
    class_management = models.ForeignKey('School_class', verbose_name = 'Классное руководство')
    teacher_cabinet = models.ForeignKey('Cabinet', verbose_name = 'Кабинет')
    teacher_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету')                # максимальная нагрузка по указанному предмету

    def __str__(self):
        return (self.last_name +' '+ self.first_name +' '+ self.middle_name)