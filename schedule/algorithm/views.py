from django.shortcuts import render_to_response, render
from schedule.models import *
from random import *
import copy

monday = [0, 1, 2, 3, 4, 5, 6]
tuesday = [7, 8, 9, 10, 11, 12, 13]
wednesday = [14, 15, 16, 17, 18, 19, 20]
thursday = [21, 22, 23, 24, 25, 26, 27]
friday = [28, 29, 30, 31, 32, 33, 34]

Classes = {
     5: 29,
     6: 30,
     7: 32,
     8: 33,
     9: 33,
     10: 34,
     11: 34}

Audiences = {
     1: [8, 4, 6],
     2: [],
     3: [],
     4: [],
     5: [],
     6: [],
     7: [],
     8: [],  # спортзал
     9: [],
     10: [],
     11: [], # еще какой-ниюудь
     12: [],
     13: [],
     14: [],
     15: [],
     }

Teachers = {
      'Питеримова': [],
      'Худякова': [],
      'Васильева': [],
      'Петрова': [],
      'Салеева': [],
      'Николаева': [],
      'Тимирева': [],
      'Иванова': [],
      'Никифорова': [],
      'Иголкина': [],
      'Рыженкова': [],
      'Колодин': [],
      'Филиппова': [],
      'Сизак': [],
      'Колесник': []
    }

Subjects = {
    # для деления на группы: класс не делится - 0, группы (иностранный) - 0.5, профильный предмет - 1, классы занимаются вместе - 2

    # [0subject, 1class, 2teacher, 3audience, 4load, 5сложность, 6спаренность,
    # 7группы/профиль, 8занятость, 9номер_профиля, 10вес (определяет приоритет)]



    3: ['Англ', 9, 'Питеримова', 1, 3, 9, 0, 0.5, 0, 0],
    4: ['Англ', 9, 'Салеева', 5, 3, 6, 0, 0.5, 0, 0],
    79: ['Информатика', 9, 'Колодин', 0, 2, 7, 0, 0.5, 0, 0],

    0: ['Биология', 9, 'Никифорова', 9, 4, 7, 0, 1, 0, 1],
    92: ['Общество', 9, 'Филиппова', 11, 2, 5, 0, 1, 0, 2],
    93: ['Физика', 9, 'Сизак', 7, 3, 5, 0, 1, 0, 2],
    #
    1: ['Англ', 7, 'Питеримова', 1, 3, 10, 0, 0, 0, 0],
    2: ['Англ', 8, 'Питеримова', 1, 3, 8, 0, 0, 0, 0],
    # #

    # ------------для тестов
    # 25: ['Англ', 9, 'Колодин', 7, 3, 4, 0, 0.5, 0, 0],
    # 4: ['Англ', 9, 'Карабанова', 1, 3, 9, 0, 0.5, 0],
    # 23: ['Русский', 9, 'Пронина', 5, 3, 6, 0, 0.5, 0],
    #
    # 25: ['Русский', 10, 'Салеева', 5, 3, 6, 0, 0, 0],
    # 24: ['Русский', 9, 'Салеева', 5, 2, 6, 0],
    # 4: ['Английский', 92, 'Питеримова', 1, 3, 9, 0],
    # ------------для тестов

    5: ['Английский', 10, 'Питеримова', 1, 3, 8, 0, 0, 0, 0],
    6: ['Английский', 11, 'Питеримова', 1, 3, 8, 0, 0, 0, 0],

    7: ['О Худякова', 9, 'Худякова', 0, 1, 1, 0, 0.5, 0, 0],
    9: ['О Худякова', 10, 'Худякова',  0, 1, 1, 0, 0, 0, 0],
    10: ['О Худякова', 11, 'Худякова',  0, 1, 1, 0, 0, 0, 0],

    11: ['Английский', 5, 'Васильева', 3, 3, 9, 0, 0, 0, 0],
    12: ['Английский', 6, 'Васильева', 3, 3, 11, 0, 0, 0, 0],

    13: ['Русский', 5, 'Петрова', 4, 6, 8, 0, 0, 0, 0],
    14: ['Русский', 8, 'Петрова', 4, 2, 7, 0, 0, 0, 0],
    15: ['Русский', 10, 'Петрова', 4, 3, 9, 0, 0, 0, 0],
    16: ['Русский', 11, 'Петрова', 4, 2, 9, 0, 0, 0, 0],

    17: ['Литература', 5, 'Петрова', 4, 2, 4, 0, 0, 0, 0],
    18: ['Литература', 8, 'Петрова', 4, 3, 4, 0, 0, 0, 0],
    19: ['Литература', 10, 'Петрова', 4, 3, 8, 0, 0, 0, 0],
    20: ['Литература', 11, 'Петрова', 4, 3, 8, 0, 0, 0, 0],

    21: ['Русский', 6, 'Салеева', 5, 6, 12, 0, 0, 0, 0],
    22: ['Русский', 7, 'Салеева', 5, 4, 11, 0, 0, 0, 0],
    23: ['Русский', 9, 'Салеева', 5, 2, 6, 0, 0, 0, 0],
    #
    # 24: ['Литература', 6, 'Салеева', 5, 3, 6, 0, 0, 0, 0],
    # 25: ['Литература', 7, 'Салеева', 5, 2, 4, 0, 0, 0, 0],
    # 26: ['Литература', 9, 'Салеева', 5, 3, 7, 0, 0, 0, 0],
    #
    # 27: ['Математика', 5, 'Николаева', 6, 5, 10, 0, 0, 0, 0],
    # 28: ['Математика', 6, 'Николаева', 6, 5, 13, 0, 0, 0, 0],
    #
    # 29: ['Алгебра', 8, 'Николаева', 6, 2, 9, 0, 0, 0, 0],
    #
    # 30: ['Геометрия', 8, 'Николаева', 6, 2, 10, 0, 0, 0, 0],
    #
    # 31: ['Алгебра', 7, 'Тимирева', 7, 3, 10, 0, 0, 0, 0],
    32: ['Алгебра', 9, 'Тимирева', 7, 4, 7, 0, 0, 0, 0],
    # 33: ['Алгебра', 10, 'Тимирева', 7, 2, 10, 0, 0, 0, 0],
    # 34: ['Алгебра', 11, 'Тимирева', 7, 4, 10, 0, 0, 0, 0],
    #
    # 35: ['Геометрия', 7, 'Тимирева', 7, 2, 12, 0, 0, 0, 0],
    36: ['Геометрия', 9, 'Тимирева', 7, 2, 8, 0, 0, 0, 0],
    # 37: ['Геометрия', 10, 'Тимирева', 7, 2, 11, 0, 0, 0, 0],
    # 38: ['Геометрия', 11, 'Тимирева', 7, 2, 11, 0, 0, 0, 0],
    #
    # 39: ['Физкультура', 5, 'Иванова', 8, 3, 3, 0, 0, 0, 0],
    # 40: ['Физкультура', 6, 'Иванова', 8, 3, 4, 0, 0, 0, 0],
    # 41: ['Физкультура', 7, 'Иванова', 8, 3, 2, 0, 0, 0, 0],
    # 42: ['Физкультура', 8, 'Иванова', 8, 3, 2, 0, 0, 0, 0],
    43: ['Физкультура', 9, 'Иванова', 8, 3, 2, 0, 0, 0, 0],
    # 44: ['Физкультура', 10, 'Иванова', 8, 3, 1, 0, 0, 0, 0],
    #
    # 45: ['Биология', 5, 'Никифорова', 9, 1, 10, 0, 0, 0, 0],
    # 46: ['Биология', 6, 'Никифорова', 9, 1, 8, 0, 0, 0, 0],
    # 47: ['Биология', 7, 'Никифорова', 9, 2, 7, 0, 0, 0, 0],
    # 48: ['Биология', 8, 'Никифорова', 9, 2, 7, 0, 0, 0, 0],
    49: ['Биология', 9, 'Никифорова', 9, 2, 7, 0, 0, 0, 0],
    #
    # 50: ['Биология', 10, 'Никифорова', 9, 3, 7, 0, 0, 0, 0],
    # 51: ['Биология', 11, 'Никифорова', 9, 1, 7, 0, 0, 0, 0],
    #
    # 52: ['Химия', 8, 'Никифорова', 9, 2, 10, 0, 0, 0, 0],
    53: ['Химия', 9, 'Никифорова', 9, 2, 12, 0, 0, 0, 0],
    # 54: ['Химия', 10, 'Никифорова', 9, 1, 11, 0, 0, 0, 0],
    # 55: ['Химия', 11, 'Никифорова', 9, 1, 11, 0, 0, 0, 0],
    #
    # 56: ['География', 5, 'Никифорова', 9, 1, 7, 0, 0, 0],  # санпин по природоведению, гелграфии нет
    # 57: ['География', 6, 'Никифорова', 9, 1, 7, 0, 0, 0],
    # 58: ['География', 7, 'Никифорова', 9, 2, 6, 0, 0, 0],
    # 59: ['География', 10, 'Никифорова', 9, 2, 3, 0, 0, 0],
    #
    # 60: ['Экология', 11, 'Никифорова', 9, 1, 3, 0, 0, 0],
    #
    # 61: ['Г Иголк', 8, 'Иголкина', 10, 2, 2, 0, 0, 0, 0],
    62: ['Г Иголк', 9, 'Иголкина', 10, 2, 3, 0, 0, 0, 0],
    #
    # 63: ['Э Иголк', 11, 'Иголкина', 10, 2, 2, 0, 0, 0, 0],
    #
    # 64: ['Ч Иголк', 8, 'Иголкина', 10, 1, 6, 0, 0, 0, 0],
    #
    # 65: ['Оо', 7, 'Иголкина', 10, 2, 1, 0, 0, 0, 0],
    # 66: ['Оо', 8, 'Иголкина', 10, 2, 2, 0, 0, 0, 0],
    67: ['Оо', 9, 'Иголкина', 10, 2, 3, 0, 0, 0, 0],
    # 68: ['Оо', 10, 'Иголкина', 10, 2, 2, 0, 0, 0, 0],
    # 69: ['Оо', 11, 'Иголкина', 10, 2, 4, 0, 0, 0, 0],
    #
    70: ['История', 9, 'Рыженкова', 0, 2, 10, 0, 0, 0, 0],
    # 71: ['История', 10, 'Рыженкова', 0, 2, 5, 0, 0, 0, 0],
    # 72: ['История', 11, 'Рыженкова', 0, 2, 5, 0, 0, 0, 0],
    #
    73: ['Общество', 9, 'Рыженкова', 0, 1, 4, 0, 0, 0, 0], # не указано в санпин
    # 74: ['Общество', 10, 'Рыженкова', 0, 2, 5, 0, 0, 0, 0],
    # 75: ['Общество', 11, 'Рыженкова', 0, 2, 5, 0, 0, 0, 0],
    #
    # 76: ['Экономика', 11, 'Рыженкова', 0, 1, 6, 0, 0, 0, 0],
    #
    # 77: ['Информатика', 7, 'Колодин', 0, 1, 4, 0, 0, 0, 0],
    # 78: ['Информатика', 8, 'Колодин', 0, 2, 7, 0, 0, 0, 0],
    # 81: ['Информатика', 10, 'Колодин', 0, 1, 6, 0, 0, 0, 0],
    # 82: ['Информатика', 11, 'Колодин', 0, 1, 6, 0, 0, 0, 0],
    #
    # 83: ['ОБЖ', 7, 'Колодин', 0, 1, 3, 0, 0, 0, 0],
    # 84: ['ОБЖ', 8, 'Колодин', 0, 1, 3, 0, 0, 0, 0],
    #
    # 85: ['История', 5, 'Филиппова', 11, 2, 5, 0, 0, 0, 0],
    # 86: ['История', 6, 'Филиппова', 11, 2, 8, 0, 0, 0, 0],
    # 87: ['История', 7, 'Филиппова', 11, 2, 6, 0, 0, 0, 0],
    # 88: ['История', 8, 'Филиппова', 11, 2, 8, 0, 0, 0, 0],
    #
    # 89: ['Общество', 5, 'Филиппова', 11, 1, 6, 0, 0, 0, 0],
    # 90: ['Общество', 6, 'Филиппова', 11, 1, 9, 0, 0, 0, 0],
    # 91: ['Общество', 7, 'Филиппова', 11, 1, 9, 0, 0, 0, 0],
    # # 92: ['Общество', 8, 'Филиппова', 11, 1, 5, 0, 0, 0, 0],
    # #
    # # 93: ['Сизак Оо', 5, 'Сизак', 0, 1, 1, 0, 0, 0, 0],
    # 94: ['Сизак Оо', 6, 'Сизак', 0, 1, 1, 0, 0, 0, 0],
    # 95: ['Сизак Оо', 7, 'Сизак', 0, 1, 1, 0, 0, 0, 0],
    # 96: ['Сизак Оо', 8, 'Сизак', 0, 1, 1, 0, 0, 0, 0],
    97: ['Сизак Оо', 9, 'Сизак', 0, 1, 1, 0, 0, 0, 0],
    #
    # 98: ['М', 5, 'Колесник',  0, 1, 1, 0, 0, 0, 0],
    # 99: ['М', 6, 'Колесник',  0, 1, 1, 0, 0, 0, 0],
    # 100: ['М', 7, 'Колесник',  0, 1, 1, 0, 0, 0, 0],
    #
    # 101: ['Труды', 5, 'Колесник', 12, 2, 4, 0, 0, 0, 0],
    # 102: ['Труды', 6, 'Колесник', 12, 2, 3, 0, 0, 0, 0],
    # 103: ['Труды', 7, 'Колесник', 12, 1, 2, 0, 0, 0, 0],
    # 104: ['Труды', 8, 'Колесник', 12, 1, 1, 0, 0, 0, 0]
}

days = 5
max_hour = 7  # по санпин
hours_in_week = days*max_hour

if days == 6:
    saturday = [35, 36, 37, 38, 39, 40, 41]


def generate(request):
    args = {}
    args['c'] = list(Classes)
    args['t'] = list(Teachers)
    args['a'] = list(Audiences)
    week_hour_class = []  # матрица week-hours-classes
    week_hour_teacher = []  # матрица week-hours-teachers
    week_hour_audience = []  # матрица week-hours-audience
    args['range'] = range(hours_in_week)  # для вывода таблицы
    H = {}  # сетка расписания

    # Расставление коэфициентов и упорядочивание Subjects
    set_weight_and_sort(Subjects)

    # # объект из бд (вот так нужно будет вызывать)
    # cr = CommonRel.objects.filter(sclass=School_class.objects.filter(id=7)) # 6 класс
    # print(cr.values())


    # первоначальное заполнение сетки расписания
    for h in range((hours_in_week)*len(Classes)):
        H[h] = 1


    # таблица запрещений для классов
    for c in range(len(Classes)):
        week_hour_class.append([])
        for hour in range(1, hours_in_week+1):
            if list(Classes)[c]<7:
                if hour%7 == 0:
                    week_hour_class[c].append(0)
                else:
                    week_hour_class[c].append(1)
            if list(Classes)[c]>=7:
                week_hour_class[c].append(1)


        # распределение максимальной нагрузки по санпин
        if sum(week_hour_class[c]) > Classes[list(Classes)[c]]:
            d = sum(week_hour_class[c]) - Classes[list(Classes)[c]]
            if d == 1:
                if int(list(Classes)[c]) < 7:
                    week_hour_class[c][randrange(5, hours_in_week, max_hour)] = 0
                else:
                    week_hour_class[c][randrange(6, hours_in_week, max_hour)] = 0
            if d>1:
                ch = [6, 13, 27, 34]  # пн, вт, чт, пт
                for j in range(1, d+1):
                    r = choice(ch)
                    ch.remove(r)
                    week_hour_class[c][r] = 0
    args["week_hour_class"] = week_hour_class


    #таблица запрещений для учителей
    for t in range(len(Teachers)):
        ban = Teachers[list(Teachers)[t]]
        week_hour_teacher.append([])
        if len(ban) == 0:
            for hour in range(0, hours_in_week):
                week_hour_teacher[t].append(1)
        else:
            for hour in range(0, hours_in_week):
                if hour in ban:
                    week_hour_teacher[t].append(0)
                else:
                    week_hour_teacher[t].append(1)
    args['week_hour_teacher'] = week_hour_teacher


    #таблица запрещений для аудиторий
    for a in range(len(Audiences)):
        ban = Audiences[list(Audiences)[a]]
        week_hour_audience.append([])
        if len(ban) == 0:
            for hour in range(0, hours_in_week):
                week_hour_audience[a].append(1)
        else:
            for hour in range(0, hours_in_week):
                if hour in ban:
                    week_hour_audience[a].append(0)
                else:
                    week_hour_audience[a].append(1)
    args['week_hour_audience'] = week_hour_audience

    #===================================================================

    # расстановка предметов в сетку расписания
    for s in range(len(Subjects)):

        # параметры для групповых и профильных занятий (гр/пр, гр - групповой, пр - профильный)

        # если у гр/пр предмета нет пары, присваивается противоположное значение
        single_lesson = False
        # если у гр/пр пары предметов совпадает нарузка
        load_is_equal = True
        # текущий предмет, который первоначально расставляем в сетку, имеет бОльшую нагрузку, чем найденный ему в пару (для пр)
        current_is_bigger = False
        # отвечает за удвоение нагрузки в случаях, когда один учитель у двух групп одного класса ведет один предмет
        double = 1
        # индексы, которые требуется удалить, чтобы предмет мог стать только первым или последним уроком
        days_to_delete = []

        params = Subjects[list(Subjects)[s]]
        if params[8] != 100:
            found_lessons = []

            print('---------')
            print('это текущий предмет: ', params[0], params[1], params[2])

# ----------------------groups-------------------------
            # если предмет групповой
            if params[7] == 0.5:
                # print('params[7]=0.5')

                # начинаем с 1 чтобы учесть и текущий предмет - должно быть вместе с ним парное количество (иначе будет обработка другая)
                count_of_group_lessons = 1

                # ищем предметы, которые тоже групповые
                for lesson in range(len(Subjects)):

                    # если это предмет, для которого также требуется деление на группы
                    if Subjects[list(Subjects)[lesson]][7] == 0.5:

                        # если это текущий класс
                        if Subjects[list(Subjects)[lesson]][1] == params[1]:

                            # если это текущий предмет
                            if Subjects[list(Subjects)[lesson]][0] == params[0]:

                                # но учитель другой
                                if Subjects[list(Subjects)[lesson]][2] != params[2]:
                                    # print(Subjects[list(Subjects)[lesson]])

                                    # и если предмет еще не расставлен в сетку, тогда добавь его в список
                                    if Subjects[list(Subjects)[lesson]][8] != 100:
                                        found_lessons.append(Subjects[list(Subjects)[lesson]])
                                        count_of_group_lessons = count_of_group_lessons+1

                # print('Это то, что тоже групповое', found_lessons, count_of_group_lessons)

                # если текущий урок является групповым и пары для него нет,
                # тогда его можно будет поставить только первым и последним уроком, чтобы не было окна
                if count_of_group_lessons % 2 != 0:
                    days_to_delete = [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31,32,33]
                # else:
                    # print('+++')
                    # print(params[4], 'текущий')
                    #
                    # for lesson in range(len(found_lessons)):
                    #     print(found_lessons[lesson][4], 'другие')
                    #
                    # print('+++')

                # если у нас будет нечетное количество уроков, но их будет больше 1
                if count_of_group_lessons < 2:
                    single_lesson = True

                # если один преподаватель ведет у класса по группам, тогда нагрузка увеличивается вдвое
                if single_lesson:
                    if count_of_group_lessons % 2 != 0:
                        double = 2
                print(count_of_group_lessons)

                go(found_lessons, current_is_bigger, params, double,
                   single_lesson, week_hour_audience, week_hour_teacher,
                   week_hour_class, days_to_delete, H, s, load_is_equal)
# ----------------------end_groups-------------------------

# ----------------------profile----------------------------
            # если предмет профильный
            if params[7] == 1:
                # print('params[7]=1')

                # found_lessons, single_lesson, current_is_bigger, days_to_delete = find_lessons_for_profile(params,
                found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal = find_lessons_for_profile(params,
                                                                                                           found_lessons,
                                                                                                           single_lesson,
                                                                                                           current_is_bigger,
                                                                                                           days_to_delete,
                                                                                                           load_is_equal)
                go(found_lessons, current_is_bigger, params, double,
                   single_lesson, week_hour_audience, week_hour_teacher,
                   week_hour_class, days_to_delete, H, s, load_is_equal)
# ----------------------end_profile----------------------------

# ---------------------ordinary--------------------------------
            if params[7] == 0:
                go(found_lessons, current_is_bigger, params, double,
                   single_lesson, week_hour_audience, week_hour_teacher,
                   week_hour_class, days_to_delete, H, s, load_is_equal)
# ---------------------end_ordinary----------------------------
        single_lesson = False
        double = 1
        args['H'] = []
        args['H_teachers'] = []

        # для вывода стандартного расписания по класссам
        for v in H.values():
            if v != 1:
                if len(v) > 10:  # параметры добавляются по 10 штук
                    args['H'].append(v[0]+'/'+v[10])
                else:
                    args['H'].append(v[0])
            else:
                args['H'].append(v)

        # для вывода расписания по учителям
        for v in H.values():
            if v != 1:
                if len(v) > 10:  # параметры добавляются по 10 штук
                    args['H_teachers'].append(v[2]+'/'+v[12])
                else:
                    args['H_teachers'].append(v[2])
            else:
                args['H_teachers'].append(v)

        # print('======')

    return render_to_response("generate.html", args)

# ======================================================
# ======================================================
# ======================================================
# ----------------------functions-----------------------

# распределение нагрузки
def distribute_the_load(single_lesson, params,  week_hour_audience, week_hour_teacher, week_hour_class, found_lessons, days_to_delete, double, H, s):
    free_index, num_class, num_audience, num_teacher = find_free_indexes(params,
                                                                         week_hour_audience,
                                                                         week_hour_class,
                                                                         week_hour_teacher,
                                                                         found_lessons)


    # print('FREE_INDEX0', free_index)

    # удаляем все дни, кроме первого и последнего урока (для уроков без пары, если это групповой или профильный предмет)
    if single_lesson:
        for day in days_to_delete:
            if day in free_index:
                free_index.remove(day)

    # для большей устойчивости
    first_copy_free_index = copy.deepcopy(free_index)

    # пробуем выполнить нормы СанПиН
    free_index = sanpin(params, free_index)

    # print('FREE_INDEX', free_index)

    # если есть возможность, убираем спаренность
    if len(free_index) >= params[4]*double:
        free_index = remove_paired(free_index, num_class, H, s)
    # print(free_index)

    if len(free_index) == 0:
        free_index = first_copy_free_index

    # print('FREE_INDEX2', free_index)


    # выбор индекса дня, куда будем ставить предмет в сетку H
    hour_cell = choice(free_index)  # hour_cell -- hour_subject
    # print(hour_cell, 'hour_cell')
    key_H = (hours_in_week)*(num_class)+hour_cell  # индекс ячейки в сетке распсиания H
    H[key_H] = list(Subjects[list(Subjects)[s]])

    # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
    if len(found_lessons) == 10:
        H[key_H] = H[key_H] + found_lessons
        # print(H[key_H], 'H[key_H]')
    else:
        for les in range(len(found_lessons)):
            H[key_H] = H[key_H] + found_lessons[les]

    # расставим занятость у классов, учителей и кабинетов
    week_hour_class[num_class][hour_cell] = 0

    for index_teacher in num_teacher:
        week_hour_teacher[index_teacher][hour_cell] = 0
        # week_hour_teacher[index_teacher][hour_cell] = params[1]  #  это чтобы классы записывались в сетку, а не нули

    for index_audience in num_audience:
        # print('num_dfdf', index_audience)
        week_hour_audience[index_audience][hour_cell] = 0
        # week_hour_audience[index_audience][hour_cell] = params[1]
#---------------------------------------------------------------

# найти профильные предметы
def find_lessons_for_profile(params, found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal):
    # начинаем с 1 чтобы учесть и текущий предмет - должно быть вместе с ним парное количество (иначе будет обработка другая)
    count_of_profile_lessons = 1

    # ищем предметы, которые тоже групповые
    for lesson in range(len(Subjects)):

        # если это тоже профильный предмет
        if Subjects[list(Subjects)[lesson]][7] == 1:

            # если это текущий класс
            if Subjects[list(Subjects)[lesson]][1] == params[1]:

                # если это не тот же самый профиль (а другая половина класса задействована)
                if Subjects[list(Subjects)[lesson]][9] != params[9]:

                    # и если предмет еще не расставлен в сетку, тогда добавь его в список
                    if Subjects[list(Subjects)[lesson]][8] != 100:
                        found_lessons.append(Subjects[list(Subjects)[lesson]])


    # print('Это то, что тоже профильное', found_lessons, count_of_profile_lessons)

    if len(found_lessons) != 0:

        # этот говнокод нужно будет исправить :/
        found_lessons = found_lessons[0]
        print(found_lessons)
        count_of_profile_lessons = 2

        current_is_bigger = False
        if found_lessons[4] != params[4]:
            # print('текущий отличается от найденного на: ', params[4]-found_lessons[4])
            load_is_equal = False

            # если еще остаются часы у найденного предмета, тогда нужно их убавить у него в исходных данных
            # print('BIGGER', current_is_bigger)
            if params[4]-found_lessons[4] > 0:
                current_is_bigger = True


    # если предмету больше нечего поставить в пару, тогда его можно ставить только первым или последним уроком
    if count_of_profile_lessons % 2 != 0:
        days_to_delete = [1, 2, 3, 4, 5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31,32,33]
        single_lesson = True

    return found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal
#---------------------------------------------------------------

# Поиск подходящих часов для расстановки предмета в соотвествие с занятостью учителей, классов и кабинетоа
def find_free_indexes(params, week_hour_audience, week_hour_class, week_hour_teacher, found_lessons):
    temp = []
    count_of_classes = 1

    # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
    if len(found_lessons) == 10:
        count_of_teachers = count_of_audience = 2
    else:
        count_of_teachers = count_of_audience = len(found_lessons)+1

    # num_audience, num_teacher, num_class нужны для расстановки в сетку расписания (номер строки)

    # ================================
    # добавляем класс во временный массив
    num_class = 0
    for c in range(len(Classes)):
        # если это искомый класс
        if list(Classes)[c] == params[1]:
            temp.append(week_hour_class[c])
            break
        else:
            num_class = num_class+1

    # ================================
    # добавляем учителей
    num_teacher = [0]*count_of_teachers
    last_lesson_number = 0

    # столько раз, сколько учителей в найденных групповых уроках
    for t_number in range(len(num_teacher)):

        # ищем индекс учителя текущего предмета, его записываем первым
        if t_number == 0:

            # Вызываем функцию, которая посчитает, какую строчку добавить к temp
            add_to_temp(temp, week_hour_teacher, params, 2, num_teacher, t_number, Teachers)

        else:
            # ищем индексы учителей найденных предметов

            # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
            if len(found_lessons) == 10:
                for l in range(1):
                    add_to_temp(temp, week_hour_teacher, found_lessons, 2, num_teacher, t_number, Teachers)
                break
            else:
                for l in range(len(found_lessons)):
                    add_to_temp(temp, week_hour_teacher, found_lessons[last_lesson_number], 2, num_teacher, t_number, Teachers)
                    last_lesson_number = last_lesson_number + 1
                break
    # print(num_teacher, 'te')
    # ================================

    # добавляем кабинет
    num_audience = [0]*count_of_audience
    last_lesson_number = 0

    for a_number in range(len(num_audience)):

        # ищем индекс кабинета текущего предмета, его записываем первым
        if a_number == 0:

            # Вызываем функцию, которая посчитает, какую строчку добавить к temp
            add_to_temp(temp, week_hour_audience, params, 3, num_audience, a_number, Audiences)
        else:
            # ищем индексы кабинетов найденных предметов

            # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
            if len(found_lessons) == 10:
                for l in range(1):
                    add_to_temp(temp, week_hour_audience, found_lessons, 3, num_audience, a_number, Audiences)
                break
            else:
                for l in range(len(found_lessons)):
                    add_to_temp(temp, week_hour_audience, found_lessons[last_lesson_number], 3, num_audience, a_number, Audiences)
                    last_lesson_number = last_lesson_number + 1
                break
    # print('func_num', num_audience)

    # ================================

    # массив для подсчета результата логического перемножения
    r = []

    # транспонирование матрицы (удобнее логически перемножать)
    temp_t = list(zip(*temp))

    for i in range(len(temp_t)):
        if temp_t[i][0] & temp_t[i][1] & temp_t[i][2]:
            r.append(1)
        else:
            r.append(0)

    # индексы тех ячеек в сетке, куда можно ставить текущее занятие (получаем из результирующего вектора)
    free_index = []

    for j in range(len(r)):
        if r[j] == 1:
            free_index.append(j)

    return free_index, num_class, num_audience, num_teacher
#---------------------------------------------------------------

# для добавления во временный массив
def add_to_temp(temp, week_hour_item, params, n, num_item, i_number, items):

    # аудитории, из которых можно выбирать
    auds = [0,1,2,3,4,5,6,8,9,11,12,13,14]  # 8, 11 - типа нельзя

    # если у преподавателя, ведущего предмет, нет привязанного кабинета (условие только для кабинетов)
    if items == Audiences:
        if params[3] == 0:
            #  надо выбрать хоть какой-нибудь кабинет (любой, кроме тех, которых нет в списке)
            i = choice(auds)
            temp.append(week_hour_item[i])
            num_item[i_number] = i
            return temp

    for i in range(len(items)):
        # print(list(items)[i])
        # ищем индекс текущего урока
        if list(items)[i] == params[n]:
            temp.append(week_hour_item[i])
            return temp
        else:
            num_item[i_number] = num_item[i_number]+1

#---------------------------------------------------------------

# Оставляем подходящие санпиновские часы
def sanpin(params, free_index):

    # делаем резервную копию: если по санпину не получится расставить, возвращаются предыдущие значения массива
    copy_free_index = copy.deepcopy(free_index)
    # print('COPY', copy_free_index)
    for_del_max = [1, 2, 3, 8, 9, 10, 15, 16, 17, 22, 23, 24, 29, 30, 31]  # уроки с наибольшей нагрузкой
    for_del_min = [0, 4, 5, 6, 7, 11, 12, 13, 14, 18, 19, 20, 21, 25, 26, 27, 28, 32, 33, 34]  # уроки с наименьшей нагрузкой

    # если урок относится к легким урокам
    if params[5] < 7:
        # удаляем все часы, в которые можно ставить тяжелые уроки
        for d in for_del_max:
            if d in free_index:
                free_index.remove(d)
    # если урок относится к тяжелым урокам
    else:
        # удаляем все часы, в которые можно ставить легкие уроки
        for d in for_del_min:
            if d in free_index:
                free_index.remove(d)

    # print('SANPIN FREE', free_index)
    if len(free_index) == 0:
        # print('если по санпину - то не хватает')
        free_index = copy_free_index

    # print(free_index, 'sanpin func')

    return free_index
#---------------------------------------------------------------

# Убираем спаренность (если есть возможность)
def remove_paired(free_index, num_class, H, s):
    # print('=== === === === ===')
    # делаем резервную копию: если без спаренности не получается расставить, возвращаются предыдущие значения массива
    copy_free_index = copy.deepcopy(free_index)

    # пробегаем по всем возможным часам в сетке расписания
    for index in range(0, hours_in_week):

        # Находим, в какой ячейке H текущий предмет у конкретного класса
        index_in_H = hours_in_week*(num_class)+index

        # Если там стоит какое-либо значение
        if H[index_in_H] != 1:

            # если там тот же предмет, что мы хотим поставить
            if H[index_in_H][0] == Subjects[list(Subjects)[s]][0]:

                # находим индекс этого предмета в сетке от 0 до 34 и индексы дня, в который стоит данный предмет
                same_subject = index_in_H - hours_in_week*(num_class)
                # print('index_in_H', index_in_H)
                # print('same_subject', same_subject)
                day = day_of_week(same_subject)

                # нужно убрать день, в котором уже есть этот предмет
                if list(set(free_index) & set(day)):
                    intersection = list(set(free_index) & set(day))
                    # print('intersection', intersection)

                    for item in intersection:
                        free_index.remove(item)
                # если этого дня в свободных индексах нет, тогда удалить соседние
                else:
                    if same_subject-1 in free_index:
                        free_index.remove(same_subject-1)
                    if same_subject+1 in free_index:
                        free_index.remove(same_subject+1)

            # print('free', free_index)
            if len(free_index) == 0:
                free_index = copy_free_index

    # print(free_index, 'sanpin func')
    # print('=== === === === ===')

    return free_index
#---------------------------------------------------------------
# ставим пометку, о том, что урок расставлен или остались еще часы
def mark_lesson(found_lessons, load_is_equal, current_is_bigger, params):
    # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
    if len(found_lessons) == 10:
        # print('-----')
        # print('len(found_lessons)', len(found_lessons))
        # print(load_is_equal)
        # если нагрузка у предметов равна, просто поставь отметку, чтобы их больше не трогать
        if load_is_equal:
            found_lessons[8] = 100
        else:
            # иначе проверяем у кого нагрузка больше, у текущего предмета или у найденного
            # если у текущего больше - тогда убираем найденный предмет, вся его нагрузка расставлена
            # print(current_is_bigger)
            if current_is_bigger:
                found_lessons[8] = 100
            else:
                # уменьшаем нагрузку найденного предмета, оставляя только не расставленные часы
                found_lessons[4] = found_lessons[4]-params[4]
                # print('+')
                # print('У НАЙДЕННОГО осталось расставить ', found_lessons[4], ' часов')
                # print('+')
                # print('=+=+=+')
                # for lesson in range(len(Subjects)):
                #     if Subjects[list(Subjects)[lesson]] == found_lessons:
                #         print(Subjects[list(Subjects)[lesson]])
                #         print(found_lessons)
                #         print(Subjects[list(Subjects)[lesson]][8])
                # print('=+=+=+')
    else:
        # print('-----')
        # print('len(found_lessons)', len(found_lessons))
        # print('-----')
        for subject in range(len(found_lessons)):
            # если нагрузка у предметов равна, просто поставь отметку, чтобы их больше не трогать
            if load_is_equal:
                found_lessons[subject][8] = 100
            else:
                # иначе проверяем у кого нагрузка больше, у текущего предмета или у найденного
                # если у текущего больше - тогда убираем найденный предмет, вся его нагрузка расставлена
                if current_is_bigger:
                    found_lessons[subject][8] = 100
                else:
                    # уменьшаем нагрузку найденного предмета, оставляя только не расставленные часы
                    found_lessons[subject][4] = found_lessons[subject][4]-params[4]
                    # print('+')
                    # print('осталось расставить ', found_lessons[subject][4], ' часов')
                    # print('+')
#-----------------------------------

# запускает расстановку нагрузки со всеми предварительными действиями
def go(found_lessons,
       current_is_bigger,
       params, double,
       single_lesson,
       week_hour_audience,
       week_hour_teacher,
       week_hour_class,
       days_to_delete,
       H, s, load_is_equal):

    # print('go', params[0], params[1])
    # print('double', double)
    # print('current_is_bigger', current_is_bigger)
    # print('single_lesson', single_lesson)

    # учет нагрузки (сколько уроков расставить)
    if len(found_lessons) != 0:
        if current_is_bigger:
            limit = found_lessons[4]*double
        else:
            limit = params[4]*double
    else:
        limit = params[4]*double
    # print('limit', limit)

    # начинаем рассставлять в соотвествии с нагрузкой
    for load in range(limit):

        distribute_the_load(single_lesson,
                            params,
                            week_hour_audience,
                            week_hour_teacher,
                            week_hour_class,
                            found_lessons,
                            days_to_delete,
                            double, H, s)
    mark_lesson(found_lessons, load_is_equal, current_is_bigger, params)

    # запустить функцию, чтоб дорасставлялись остальные часы, оставшиеся у текущего урока
    if len(found_lessons) != 0:
        if current_is_bigger:
            # print('=+=+=+')
            # print(Subjects[list(Subjects)[s]])
            #     # for lesson in range(len(Subjects)):
            #     #     if Subjects[list(Subjects)[lesson]] == found_lessons:
            #     #         print(Subjects[list(Subjects)[lesson]])
            #     #         print(found_lessons)
            #     #         print(Subjects[list(Subjects)[lesson]][8])
            # print('=+=+=+')
            params[4] = params[4]-found_lessons[4]
            # print(Subjects[list(Subjects)[s]])
            single_lesson = True
            found_lessons = []
            found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal = find_lessons_for_profile(params,
                                                                                                   found_lessons,
                                                                                                   single_lesson,
                                                                                                   current_is_bigger,
                                                                                                   days_to_delete,
                                                                                                   load_is_equal)
            # print('МЫ ВОТ ЗДЕСЬ')
            # если урок найденный уже расставлен, а урок текущий еще не до конца - дорасставляем оставшиеся часы
            go(found_lessons, current_is_bigger, params, double,
                   single_lesson, week_hour_audience, week_hour_teacher,
                   week_hour_class, days_to_delete, H, s, load_is_equal)
        else:
            Subjects[list(Subjects)[s]][8] = 100


#-----------------------------------
def day_of_week(hour):
    day = []
    if hour in monday:
        day = monday
    if hour in tuesday:
        day = tuesday
    if hour in wednesday:
        day = wednesday
    if hour in thursday:
        day = thursday
    if hour in friday:
        day = friday
    return day
#-------------------------------------

# [0subject, 1class, 2teacher, 3audience, 4load, 5сложность, 6спаренность,
    # 7группы/профиль, 8занятость, 9номер_профиля, 10вес (определяет приоритет)]

# назначение коэфициентов и упорядочивание, ключ будет меняться на коэффициент (?)
def set_weight_and_sort(Subjects):
    # print(list(Subjects.values())) - выводит значения

    coef = []
    # это надо переделать с Teachers
    TeachersStaff = {
          'Питеримова': False,
          'Худякова': False,
          'Васильева': False,
          'Петрова': False,
          'Салеева': False,
          'Николаева': False,
          'Тимирева': False,
          'Иванова': False,
          'Никифорова': False,
          'Иголкина': False,
          'Рыженкова': True,
          'Колодин': True,
          'Филиппова': False,
          'Сизак': False,
          'Колесник': False
        }

    for subject in list(Subjects.values()):

        print(subject)

        for teacher in list(TeachersStaff):

            # если учитель этого предмета относится к совместителям, коэфициент = 100, иначе - 1+
            if subject[2] == teacher:
                ind = len(coef)
                if TeachersStaff[teacher]:
                    coef.insert(ind, 100)
                else:
                    coef.insert(ind, 1)

                # если предмет относится к профильным, умножь на 5, иначе - на 2+
                print(ind, 'ind')
                if subject[7] == 1:

                    coef[ind] = coef[ind]*5
                else:
                    # если предмет относится к групповым, умножь на 4, иначе - на 2
                    if subject[7] == 0.5:
                        coef[ind] = coef[ind]*4
                    else:
                        coef[ind] = coef[ind]*2

                # если это 5, 9 и 11 класс, умножь на 5, если 6 - на 4, если 10 - на 3, если 7, 8 - на 2
                if subject[1] == 5:
                    coef[ind] = coef[ind]*7
                if subject[1] == 11:
                    coef[ind] = coef[ind]*6
                if subject[1] == 9:
                    coef[ind] = coef[ind]*5
                if subject[1] == 6:
                    coef[ind] = coef[ind]*4
                if subject[1] == 10:
                    coef[ind] = coef[ind]*3
                if subject[1] == 7:
                    coef[ind] = coef[ind]*2
                if subject[1] == 8:
                    coef[ind] = coef[ind]*1

                # умножь на params[5]/10, где params[5] - санпин
                coef[ind] = coef[ind]*(subject[5]/10)

                # умножь на load/10
                coef[ind] = coef[ind] + (subject[4]/10)

                # если дефицитный кабинет - умножь на 2

                ind = ind+1


        print(sorted(coef))














