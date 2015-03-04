from django.db import models

# class Administration(models.Model):
#     class Meta():
#         db_table = 'admin'
#     login = models.CharField(max_length=15)
#     password = models.CharField(max_length=20)


class school_class(models.Model):
    classname = models.CharField(max_length=4)
   # class_teacher =

# Класс
#     номер (5а)
#     класс рук
#     кабинет
#     нагрузка?
#
# Учитель
#     ФИО
#     Предмет (1уч - мн предметов)
#     Кабинет
#     Часы(нагрузка)
#
# Предмет
#     название
#     сложность
#
# Кабинет
#     номер
#     учитель
#

