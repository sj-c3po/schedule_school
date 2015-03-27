# -*- coding: utf-8 -*-

from django.db import models


class School_class(models.Model):
    class Meta():
        db_table = 'school_class'
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    class_name = models.CharField('Название класса', max_length=10) # 11а и хватит (юникод?)
    class_max_load = models.IntegerField('Максимальная недельная нагрузка класса')

    def __str__(self):
        return self.class_name


class Cabinet(models.Model):
    class Meta():
        db_table = 'cabinet'
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    cabinet_number = models.CharField('Номер кабинета', max_length=10)  # char - а вдруг там буквы?

    def __str__(self):
        return self.cabinet_number


class Subject(models.Model):
    class Meta():
        db_table = 'subject'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    subject_name = models.CharField('Название предмета', max_length=30)

    def __str__(self):
        return self.subject_name


class Teacher(models.Model):
    class Meta():
        db_table = 'teacher'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    middle_name = models.CharField('Отчество', max_length=50)
    class_management = models.ForeignKey('School_class', null=True, blank=True, verbose_name='Классное руководство')
    teacher_cabinet = models.ForeignKey('Cabinet', null=True, blank=True,  verbose_name='Кабинет')    # кабинет либо есть, либо нет, учитель не бегает туда-сюда

    def __str__(self):
        return (self.last_name +' '+ self.first_name +' '+ self.middle_name)


# соединительные таблицы
class SubjectTeacherRel(models.Model):
    class Meta():
        db_table = 'subject_teacher_rel'
        verbose_name = 'Учитель-Предмет'
        verbose_name_plural = 'Учитель-Предмет'

    subject = models.ForeignKey(Subject, verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
    teacher_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету')                # максимальная нагрузка по указанному предмету


class CommonRel(models.Model):
    class Meta():
        db_table = 'common_rel'
        verbose_name = 'Класс-Предмет'
        verbose_name_plural = 'Класс-Предмет'

    sclass = models.ForeignKey(School_class, verbose_name='Класс')
    subject = models.ForeignKey(Subject, verbose_name='Предмет')
    cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет')
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
    subject_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету')
