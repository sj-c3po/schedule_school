from django.shortcuts import render_to_response, render
from random import *
import copy

Classes = {5: 29,
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
     8: [],
     9: [],
     10: [],
     11: [],
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

    # [0subject, 1class, 2teacher, 3audience, 4load, 5сложность, 6спаренность, 7группы/профиль, 8занятость, 9номер_профиля]



    49: ['Биология', 9, 'Никифорова', 9, 2, 7, 0, 1, 0, 1],
    92: ['Общество', 9, 'Филиппова', 11, 2, 5, 0, 1, 0, 2],
    # 93: ['Физика', 9, 'Филиппова', 11, 2, 5, 0, 1, 0, 3],

    # 1: ['Англ', 7, 'Питеримова', 1, 3, 10, 0, 0, 0],
    # 2: ['Англ', 8, 'Питеримова', 1, 3, 8, 0, 0, 0],
    3: ['Англ', 9, 'Питеримова', 1, 3, 9, 0, 0.5, 0, 0],
    4: ['Англ', 9, 'Салеева', 5, 3, 6, 0, 0.5, 0, 0],
    # # 25: ['Англ', 9, 'Колодин', 7, 3, 4, 0, 0.5, 0],
    # # 4: ['Англ', 9, 'Карабанова', 1, 3, 9, 0, 0.5, 0],
    # # 23: ['Русский', 9, 'Пронина', 5, 3, 6, 0, 0.5, 0],
    #
    # # 25: ['Русский', 10, 'Салеева', 5, 3, 6, 0, 0, 0],
    # # 24: ['Русский', 9, 'Салеева', 5, 2, 6, 0],
    # # 4: ['Английский', 92, 'Питеримова', 1, 3, 9, 0],
    # 5: ['Английский', 10, 'Питеримова', 1, 3, 8, 0, 0, 0],
    # 6: ['Английский', 11, 'Питеримова', 1, 3, 8, 0, 0, 0],
    #
    # # 7: ['О', 9, 'Худякова', 2, 1, '-', 0],
    # # # 8: ['О', 92, 'Худякова', 2, 1, '-', 0],
    # # 9: ['О', 10, 'Худякова', 2, 1, '-', 0],
    # # 10: ['О', 11, 'Худякова', 2, 1, '-', 0],
    # #
    # 11: ['Английский', 5, 'Васильева', 3, 3, 9, 0, 0, 0],
    # 12: ['Английский', 6, 'Васильева', 3, 3, 11, 0, 0, 0],
    # # # #
    # 13: ['Русский', 5, 'Петрова', 4, 6, 8, 0, 0, 0],
    # 14: ['Русский', 8, 'Петрова', 4, 2, 7, 0, 0, 0],
    # 15: ['Русский', 10, 'Петрова', 4, 3, 9, 0, 0, 0],
    # 16: ['Русский', 11, 'Петрова', 4, 2, 9, 0, 0, 0],
    # # # #
    # 17: ['Литература', 5, 'Петрова', 4, 2, 4, 0, 0, 0],
    # 18: ['Литература', 8, 'Петрова', 4, 3, 4, 0, 0, 0],
    # 19: ['Литература', 10, 'Петрова', 4, 3, 8, 0, 0, 0],
    # 20: ['Литература', 11, 'Петрова', 4, 3, 8, 0, 0, 0],
    # # # # #
    21: ['Русский', 6, 'Салеева', 5, 6, 12, 0, 0, 0],
    22: ['Русский', 7, 'Салеева', 5, 4, 11, 0, 0, 0],
    23: ['Русский', 9, 'Салеева', 5, 2, 6, 0, 0, 0],
    # # # # #
    # 24: ['Литература', 6, 'Салеева', 5, 3, 6, 0, 0, 0],
    # 25: ['Литература', 7, 'Салеева', 5, 2, 4, 0, 0, 0],
    # 26: ['Литература', 9, 'Салеева', 5, 3, 7, 0, 0, 0],
    # # # #
    # 27: ['Математика', 5, 'Николаева', 6, 5, 10, 0, 0, 0],
    # 28: ['Математика', 6, 'Николаева', 6, 5, 13, 0, 0, 0],
    # # # # #
    # 29: ['Алгебра', 8, 'Николаева', 6, 2, 9, 0, 0, 0],
    # # # #
    # 30: ['Геометрия', 8, 'Николаева', 6, 2, 10, 0, 0, 0],
    # # # # #
    # 31: ['Алгебра', 7, 'Тимирева', 7, 3, 10, 0, 0, 0],
    # 32: ['Алгебра', 9, 'Тимирева', 7, 4, 7, 0, 0, 0],
    # 33: ['Алгебра', 10, 'Тимирева', 7, 2, 10, 0, 0, 0],
    # 34: ['Алгебра', 11, 'Тимирева', 7, 4, 10, 0, 0, 0],
    # # # #
    # 35: ['Геометрия', 7, 'Тимирева', 7, 2, 12, 0, 0, 0],
    # 36: ['Геометрия', 9, 'Тимирева', 7, 2, 8, 0, 0, 0],
    # 37: ['Геометрия', 10, 'Тимирева', 7, 2, 11, 0, 0, 0],
    # 38: ['Геометрия', 11, 'Тимирева', 7, 2, 11, 0, 0, 0],
    # #
    # 39: ['Физкультура', 5, 'Иванова', 8, 3, 3, 0, 0, 0],
    # 40: ['Физкультура', 6, 'Иванова', 8, 3, 4, 0, 0, 0],
    # 41: ['Физкультура', 7, 'Иванова', 8, 3, 2, 0, 0, 0],
    # 42: ['Физкультура', 8, 'Иванова', 8, 3, 2, 0, 0, 0],
    # 43: ['Физкультура', 9, 'Иванова', 8, 3, 2, 0, 0, 0],
    # 44: ['Физкультура', 10, 'Иванова', 8, 3, 1, 0, 0, 0],
    # # # #
    # 45: ['Биология', 5, 'Никифорова', 9, 1, 10, 0, 0, 0],
    # 46: ['Биология', 6, 'Никифорова', 9, 1, 8, 0, 0, 0],
    # 47: ['Биология', 7, 'Никифорова', 9, 2, 7, 0, 0, 0],
    # 48: ['Биология', 8, 'Никифорова', 9, 2, 7, 0, 0, 0],
    # 49: ['Биология', 9, 'Никифорова', 9, 2, 7, 0, 0, 0],


    # 50: ['Биология', 10, 'Никифорова', 9, 3, 7, 0, 0, 0],
    # 51: ['Биология', 11, 'Никифорова', 9, 1, 7, 0, 0, 0],
    # # # # #
    # 52: ['Химия', 8, 'Никифорова', 9, 2, 10, 0, 0, 0],
    # 53: ['Химия', 9, 'Никифорова', 9, 2, 12, 0, 0, 0],
    # 54: ['Химия', 10, 'Никифорова', 9, 1, 11, 0, 0, 0],
    # 55: ['Химия', 11, 'Никифорова', 9, 1, 11, 0, 0, 0],
    # # # # #
    # 56: ['География', 5, 'Никифорова', 9, 1, 7, 0, 0, 0],  # санпин по природоведению, гелграфии нет
    # 57: ['География', 6, 'Никифорова', 9, 1, 7, 0, 0, 0],
    # 58: ['География', 7, 'Никифорова', 9, 2, 6, 0, 0, 0],
    # 59: ['География', 10, 'Никифорова', 9, 2, 3, 0, 0, 0],
    # # # # #
    # 60: ['Экология', 11, 'Никифорова', 9, 1, 3, 0, 0, 0],
    # # #
    # # 61: ['Г', 8, 'Иголкина', 10, 2, '-', 0],
    # # 62: ['Г', 9, 'Иголкина', 10, 2, '-', 0],
    # # #
    # # 63: ['Э', 11, 'Иголкина', 10, 2, '-', 0],
    # # #
    # # # 64: ['Ч', 8, 'Иголкина', 10, 1, '-', 0],
    # # #
    # # # 65: ['Оо', 7, 'Иголкина', 10, 2, '-', 0],
    # # # 66: ['Оо', 8, 'Иголкина', 10, 2, '-', 0],
    # # # 67: ['Оо', 9, 'Иголкина', 10, 2, '-', 0],
    # # # 68: ['Оо', 10, 'Иголкина', 10, 2, '-', 0],
    # # # 69: ['Оо', 11, 'Иголкина', 10, 2, '-', 0],
    # # #
    # # # 70: ['История', 9, 'Рыженкова', '-', 2, 10, 0],
    # # # 71: ['История', 10, 'Рыженкова', '-', 2, 5, 0],
    # # # 72: ['История', 11, 'Рыженкова', '-', 2, 5, 0],
    # # #
    # # # 73: ['Общество', 9, 'Рыженкова', '-', 1, '-', 0], # не указано в санпин
    # # # 74: ['Общество', 10, 'Рыженкова', '-', 2, 5, 0],
    # # # 75: ['Общество', 11, 'Рыженкова', '-', 2, 5, 0],
    # # #
    # # # 76: ['Экономика', 11, 'Рыженкова', '-', 1, 6, 0],
    # # #
    # # # 77: ['Информатика', 7, 'Колодин', '-', 1, 4, 0],
    # # # 78: ['Информатика', 8, 'Колодин', '-', 2, 7, 0],
    # # # 79: ['Информатика', 9, 'Колодин', '-', 2, 7, 0],
    # # # # 80: ['Информатика', 92, 'Колодин', '-', 2, 7, 0],
    # # # 81: ['Информатика', 10, 'Колодин', '-', 1, 6, 0],
    # # # 82: ['Информатика', 11, 'Колодин', '-', 1, 6, 0],
    # # #
    # # # 83: ['ОБЖ', 7, 'Колодин', '-', 1, 3, 0],
    # # # 84: ['ОБЖ', 8, 'Колодин', '-', 1, 3, 0],
    # #
    # 85: ['История', 5, 'Филиппова', 11, 2, 5, 0, 0, 0],
    # 86: ['История', 6, 'Филиппова', 11, 2, 8, 0, 0, 0],
    # 87: ['История', 7, 'Филиппова', 11, 2, 6, 0, 0, 0],
    # 88: ['История', 8, 'Филиппова', 11, 2, 8, 0, 0, 0],
    #
    # 89: ['Общество', 5, 'Филиппова', 11, 1, 6, 0, 0, 0],
    # 90: ['Общество', 6, 'Филиппова', 11, 1, 9, 0, 0, 0],
    # 91: ['Общество', 7, 'Филиппова', 11, 1, 9, 0, 0, 0],
    # 92: ['Общество', 8, 'Филиппова', 11, 1, 5, 0, 0, 0],
    # # #
    # # # # 93: ['Сизак Оо', 5, 'Сизак', '-', 1, '-', 0],
    # # # # 94: ['Сизак Оо', 6, 'Сизак', '-', 1, '-', 0],
    # # # # 95: ['Сизак Оо', 7, 'Сизак', '-', 1, '-', 0],
    # # # # 96: ['Сизак Оо', 8, 'Сизак', '-', 1, '-', 0],
    # # # # 97: ['Сизак Оо', 9, 'Сизак', '-', 1, '-', 0],
    # # # #
    # # # # 98: ['М', 5, 'Колесник', '-', 1, '-', 0],
    # # # # 99: ['М', 6, 'Колесник', '-', 1, '-', 0],
    # # # # 100: ['М', 7, 'Колесник', '-', 1, '-', 0],
    # # # #
    # 101: ['Труды', 5, 'Колесник', 12, 2, 4, 0, 0, 0],
    # 102: ['Труды', 6, 'Колесник', 12, 2, 3, 0, 0, 0],
    # 103: ['Труды', 7, 'Колесник', 12, 1, 2, 0, 0, 0],
    # 104: ['Труды', 8, 'Колесник', 12, 1, 1, 0, 0, 0]
}

days = 5
max_hour = 7  # по санпин
hours_in_week = days*max_hour
monday = [0, 1, 2, 3, 4, 5, 6]
tuesday = [7, 8, 9, 10, 11, 12, 13]
wednesday = [14, 15, 16, 17, 18, 19, 20]
thursday = [21, 22, 23, 24, 25, 26, 27]
friday = [28, 29, 30, 31, 32, 33, 34]

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

    # нужен для определения, единственный ли предмет или он нечетный (для групповых предметов)
    single_lesson = False
    double = 1
    days_to_delete = []

    # расстановка предметов в сетку расписания
    for s in range(len(Subjects)):
        params = Subjects[list(Subjects)[s]]
        if params[8] != 100:
            found_lessons = []

            print('---------')
            print('это текущий предмет: ', params[0], params[1], params[2])

# ----------------------groups-------------------------
            # если предмет групповой
            if params[7] == 0.5:
                print('params[7]=0.5')

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
                                    print(Subjects[list(Subjects)[lesson]])

                                    # и если предмет еще не расставлен в сетку, тогда добавь его в список
                                    if Subjects[list(Subjects)[lesson]][8] != 100:
                                        found_lessons.append(Subjects[list(Subjects)[lesson]])
                                        count_of_group_lessons = count_of_group_lessons+1

                print('Это то, что тоже групповое', found_lessons, count_of_group_lessons)

                # если текущий урок является групповым и пары для него нет,
                # тогда его можно будет поставить только первым и последним уроком, чтобы не было окна

                if count_of_group_lessons % 2 == 0:
                    print('+++')
                    print(params[4], 'текущий')

                    for lesson in range(len(found_lessons)):
                        print(found_lessons[lesson][4], 'другие')

                    print('+++')
                else:
                    days_to_delete = [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31,32,33]

                # если у нас будет нечетное количество уроков, но их будет больше 1
                if count_of_group_lessons < 2:
                    single_lesson = True

                # если один преподаватель ведет у класса по группам, тогда нагрузка увеличивается вдвое
                if single_lesson:
                    if count_of_group_lessons % 2 != 0:
                        double = 2
# ----------------------end_groups-------------------------

# ----------------------profile----------------------------
            # если предмет профильный
            if params[7] == 1:
                print('params[7]=1')

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
                                    count_of_profile_lessons = count_of_profile_lessons+1


                print('Это то, что тоже профильное', found_lessons, count_of_profile_lessons)

                # этот говнокод нужно будет исправить :/
                found_lessons = found_lessons[0]
                print(found_lessons)

                # если предмету больше нечего поставить в пару, тогда его можно ставить только первым или последним уроком
                if count_of_profile_lessons % 2 != 0:
                    days_to_delete = [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31,32,33]
                    single_lesson = True
# ----------------------end_profile----------------------------

            # учет нагрузки (сколько уроков расставить)
            print(double, 'double-нагрузка')
            print(params[4]*double, 'нагрузка')

            for load in range(params[4]*double):

                free_index, num_class, num_audience, num_teacher = find_free_indexes(params,
                                                                                     week_hour_audience,
                                                                                     week_hour_class,
                                                                                     week_hour_teacher,
                                                                                     found_lessons)
                # print(num_audience, num_class, num_teacher, 'Num')

                # удаляем все дни, кроме первого и последнего урока (для уроков без пары)
                if single_lesson:
                    for day in days_to_delete:
                        if day in free_index:
                            free_index.remove(day)

                free_index = sanpin(params, free_index)

                if len(free_index) > params[4]*double:
                    free_index = remove_paired(free_index, num_class, H, s)

                print(free_index)

                # выбор индекса дня, куда будем ставить предмет в сетку H
                hour_cell = choice(free_index)  # hour_cell -- hour_subject
                print(hour_cell, 'hour_cell')
                key_H = (hours_in_week)*(num_class)+hour_cell  # индекс ячейки в сетке распсиания H
                H[key_H] = list(Subjects[list(Subjects)[s]])

                # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
                if len(found_lessons) == 10:
                    H[key_H] = H[key_H] + found_lessons
                    print(H[key_H], 'H[key_H]')
                else:
                    for les in range(len(found_lessons)):
                        H[key_H] = H[key_H] + found_lessons[les]

                # расставим занятость у классов, учителей и кабинетов
                week_hour_class[num_class][hour_cell] = 0

                for index_teacher in num_teacher:
                    week_hour_teacher[index_teacher][hour_cell] = 0
                    # week_hour_teacher[index_teacher][hour_cell] = params[1]  #  это чтобы классы записывались в сетку, а не нули

                for index_audience in num_audience:
                    week_hour_audience[index_audience][hour_cell] = 0
                    # week_hour_audience[index_audience][hour_cell] = params[1]

            # предмет больше не должен задействоваться
            Subjects[list(Subjects)[s]][8] = 100

            # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
            if len(found_lessons) == 10:
                found_lessons[8] = 100
            else:
                for subject in range(len(found_lessons)):
                    found_lessons[subject][8] = 100

        single_lesson = False
        double = 1
        args['H'] = []
        args['H_teachers'] = []

        # для вывода стандартного расписания по класссам
        for v in H.values():
            if v != 1:
                print('v', v)
                # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
                if len(found_lessons) == 10:
                    print('found_lessons', found_lessons)
                    args['H'].append(v[0]+'/'+v[10])
                    print('args["H"]', args['H'])
                else:
                    if len(v) > 9:  # параметры добавляются по 9 штук
                        args['H'].append(v[0]+'/'+v[10])
                    else:
                        args['H'].append(v[0])
            else:
                args['H'].append(v)

        # для вывода расписания по учителям
        for v in H.values():
            if v != 1:
                # print('v', v)

                 # говнокод! (если массив не [][][], а [], нужно делать так, чтоб его длину выдавало единицей)
                if len(found_lessons) == 10:
                    args['H_teachers'].append(v[2])
                else:
                    if len(v) > 9:  # параметры добавляются по 9 штук
                        args['H_teachers'].append(v[2]+'/'+v[12])
                    else:
                        args['H_teachers'].append(v[2])
            else:
                args['H_teachers'].append(v)

        print('======')

    return render_to_response("generate.html", args)


# ----------------------functions-----------------------

# Поиск подходящих часов для расстановки предмета в соотвествие с занятостью учителей, классов и кабинетоа
def find_free_indexes(params, week_hour_audience, week_hour_class, week_hour_teacher, found_lessons):
    temp = []
    print(found_lessons)

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



    print(num_teacher)
    # ================================

    # добавляем кабинет
    num_audience = [0]*count_of_audience
    last_lesson_number = 0
    # print(num_audience, 'num_audience0')

    for a_number in range(len(num_audience)):

        # ищем индекс кабинета текущего предмета, его записываем первым
        if a_number == 0:

            # Вызываем функцию, которая посчитает, какую строчку добавить к temp
            add_to_temp(temp, week_hour_audience, params, 3, num_audience, a_number, Audiences)
            # print(temp)
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


# для добавления во временный массив
def add_to_temp(temp, week_hour_item, params, n, num_item, i_number, items):

    for i in range(len(items)):
        # print(list(items)[i])
        # ищем индекс текущего урока
        if list(items)[i] == params[n]:
            temp.append(week_hour_item[i])
            return temp
        else:
            num_item[i_number] = num_item[i_number]+1


# Оставляем подходящие санпиновские часы
def sanpin(params, free_index):

    # делаем резервную копию: если по санпину не получится расставить, возвращаются предыдущие значения массива
    copy_free_index = copy.deepcopy(free_index)
    for_del_max = [1, 2, 3, 8, 9, 10, 15, 16, 17, 22, 23, 24, 29, 30, 31]  # уроки с наибольшей нагрузкой
    for_del_min = [0, 4, 5, 6, 7, 11, 12, 13, 14, 18, 19, 20, 21, 25, 26, 27, 28, 32, 33, 34]  # уроки с наименьшей нагрузкой

    # если урок относится к легким урокам
    if params[5] < 7:
        # удаляем все часы, в которые можно ставить тяжелые уроки
        for d in for_del_max:
            if d in free_index:
                free_index.remove(d)
        if len(free_index) == 0:
            print('если по санпину - то не хватает')
            free_index = copy_free_index

    # если урок относится к тяжелым урокам
    else:
        # удаляем все часы, в которые можно ставить легкие уроки
        for d in for_del_min:
            if d in free_index:
                free_index.remove(d)
        if len(free_index) == 0:
            print('если по санпину - то не хватает')
            free_index = copy_free_index

    print(free_index, 'sanpin func')

    return free_index


# Убираем спаренность (если есть возможность)
def remove_paired(free_index, num_class, H, s):
    print('=== === === === ===')
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
                print('index_in_H', index_in_H)
                print('same_subject', same_subject)
                day = day_of_week(same_subject)

                # нужно убрать день, в котором уже есть этот предмет
                if list(set(free_index) & set(day)):
                    intersection = list(set(free_index) & set(day))
                    print('intersection', intersection)

                    for item in intersection:
                        free_index.remove(item)
                # если этого дня в свободных индексах нет, тогда удалить соседние
                else:
                    if same_subject-1 in free_index:
                        free_index.remove(same_subject-1)
                    if same_subject+1 in free_index:
                        free_index.remove(same_subject+1)

            print('free', free_index)
            if len(free_index) == 0:
                free_index = copy_free_index

    print(free_index, 'sanpin func')
    print('=== === === === ===')

    return free_index


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


# косяки:
# 1. спаренность плохо работает, пока не могу это убрать из-за выставления предметам признака расставленности - param[8]=100