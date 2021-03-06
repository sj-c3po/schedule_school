# -*- coding: utf-8 -*-

from django.db import models


class School_class(models.Model):
    class Meta():
        db_table = 'school_class'
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['parallel', 'letter']

    parallel = models.IntegerField('Параллель')
    letter = models.CharField('Буква', max_length=1, null=True, blank=True)
    class_max_load = models.IntegerField('Максимальная недельная нагрузка класса')

    def __str__(self):
        return (str(self.parallel)+self.letter)

    def parallel_letter(self):
        return (str(self.parallel)+self.letter)


class Cabinet(models.Model):
    class Meta():
        db_table = 'cabinet'
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    cabinet_number = models.CharField('Номер кабинета', max_length=10)  # char - а вдруг там буквы?
    specific = models.BooleanField('Специфичный', default=False)

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
    # class_management = models.ForeignKey('School_class', null=True, blank=True, verbose_name='Классное руководство')
    teacher_cabinet = models.ForeignKey('Cabinet', null=True, blank=True,  verbose_name='Кабинет')    # кабинет либо есть, либо нет, учитель не бегает туда-сюда
    staff_type = models.BooleanField('Совместитель', default=False)
    ban_hours = models.CommaSeparatedIntegerField('Нерабочие часы', max_length=100, null=True, blank=True, default=None)

    def __str__(self):
        return (self.last_name +' '+ self.first_name +' '+ self.middle_name)


# соединительные таблицы
# class SubjectTeacherRel(models.Model):
#     class Meta():
#         db_table = 'subject_teacher_rel'
#         verbose_name = 'Учитель-Предмет'
#         verbose_name_plural = 'Учитель-Предмет'
#
#     subject = models.ForeignKey(Subject, verbose_name='Предмет')
#     teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
#     teacher_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету')                # максимальная нагрузка по указанному предмету
#     def __str__(self):
#         return (self.subject)

class Division(models.Model):
    class Meta():
        db_table = 'division'
        verbose_name = 'Вид деления'
        verbose_name_plural = 'Виды деления'

    division = models.CharField(max_length=50)

    def __str__(self):
        return (self.division)


class Class_profiles(models.Model):
    class Meta():
        # db_table = 'scope'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    profile = models.CharField(max_length=50)
    def __str__(self):
        return (self.profile)


class CommonRel(models.Model):
    class Meta():
        db_table = 'common_rel'
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебный план'
        ordering = ['sclass']

    sclass = models.ForeignKey(School_class, verbose_name='Класс')
    subject = models.ForeignKey(Subject, verbose_name='Предмет')
    cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет')
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
    subject_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету', null=True, blank=True,
                                           default=0)
    difficulty_level = models.IntegerField('Уровень сложности по СанПиН', default=1)
    division_class = models.ForeignKey(Division, verbose_name='Деление на', default=1)
    profile = models.ForeignKey(Class_profiles, verbose_name='Профиль', null=True, blank=True)

    def __str__(self):
        return (str(self.sclass.parallel)+self.sclass.letter)


class Schedule(models.Model):
    class Meta():
        db_table = 'schedule'
        verbose_name = 'Номер расписания'
        verbose_name_plural = 'Номера расписаний'
        ordering = ['-id']

    date = models.DateTimeField(verbose_name='Дата создания', null=True)

    def __str__(self):
        return (str(self.id))

class Schedule_items(models.Model):
    class Meta():
        db_table = 'schedule_items'
        verbose_name = 'Элементы расписания'
        verbose_name_plural = 'Элементы расписаний'
        ordering = ['schedule_id', 'cell_number']

    schedule_id = models.ForeignKey(Schedule, verbose_name='Расписание')
    cell_number = models.IntegerField('Номер в сетке расписания')
    # relation = models.CharField('Учитель-Класс-Предмет-Кабинет', max_length=300, blank=True, null=True)
    # length = models.IntegerField('Количество уроков в текущий час', blank=True, null=True)

    sclass = models.ForeignKey(School_class, verbose_name='Класс', null=True, blank=True)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', null=True, blank=True)
    cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель', null=True, blank=True)

    def __str__(self):
        return (str(self.id))


class Scope(models.Model):
    class Meta():
        # db_table = 'scope'
        verbose_name = 'Сфера преподавания'
        verbose_name_plural = 'Сферы преподавания'

    scope = models.CharField(max_length=50)
    def __str__(self):
        return (self.scope)






# Возможно, стоит добавить год обучения в таблицу общих связей - 2014-2015 например. Вдруг данные разных лет отличаются