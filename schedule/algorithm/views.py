from django.shortcuts import render_to_response
from random import *
import copy

# назначение коэфициентов и сортировка по значению коэфициента
def set_weight_and_sort(Subjects):

    coef = []

    for subject in list(Subjects.values()):

        for teacher in list(Teachers):

            # если учитель этого предмета относится к совместителям, коэфициент = 100, иначе - 1
            if subject[2] == teacher:
                if Teachers[teacher][0]:
                    subject[10] = 100
                else:
                    if subject[7] == 0.5:
                        subject[10] = 80
                    else:
                        if subject[7] == 0.8:
                            subject[10] = 50
                        else:
                            subject[10] = 1

                subject[10] = subject[10] + len(Teachers[teacher][1:])*5

                # если предмет относится к профильным, умножь на 4
                if subject[7] == 1:
                    subject[10] = subject[10]*25
                else:
                    # если предмет относится к групповым, умножь на 10, иначе - на 2
                    if subject[7] == 0.5:
                        subject[10] = subject[10]*10
                        # важно! групповые предметы с максимальной нагрузкой должны расставляться в первую очередь
                        if is_max_load(subject):
                            subject[10] = subject[10]+4000
                    else:
                        subject[10] = subject[10]*2

                # если это 5, 9 и 11 класс, умножь на 5, если 6 - на 4, если 10 - на 3, если 7, 8 - на 2
                if subject[1] == 5:
                    subject[10] = subject[10]*7
                if subject[1] == 11:
                    subject[10] = subject[10]*6
                if subject[1] == 9:
                    subject[10] = subject[10]*5
                if subject[1] == 6:
                    subject[10] = subject[10]*4
                if subject[1] == 10:
                    subject[10] = subject[10]*3
                if subject[1] == 7:
                    subject[10] = subject[10]*2
                if subject[1] == 8:
                    subject[10] = subject[10]*1

                # умножь на params[5]/10, где params[5] - санпин
                subject[10] = subject[10]*(subject[5]/10)

                # умножь на load*10
                subject[10] = subject[10] + (subject[4]*10)

                # если кабинет относится к дефицитным - умножь на 2
                for audience in list(Audiences):
                    if subject[3] == audience:
                        if Audiences[audience][0]:
                            subject[10] = subject[10]*2
        coef.append(subject[10])

    newList = sorted(Subjects.items(), key=lambda x: x[1][10], reverse=True)
    new = {}
    i = 0
    for key in newList:
        new[i] = key[1]
        i=i+1
    Subjects = new

    print('Отсортированные по коэфициенту предметы')
    for subj in Subjects.values():
        print(subj)


    return Subjects


def is_max_load(subject):
    for lesson in Subjects.values():
        if lesson[4] > subject[4]:
            return False
    return True


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
     11: 34
     }

# True/False - Дефицитный/Обычный
Audiences = {
     1: [False],
     2: [False],
     3: [False],
     4: [False],
     5: [False],
     6: [False],
     7: [True],
     8: [False],
     9: [False],
     10: [False],
     11: [False],
     12: [False],
     13: [False],
     14: [False],
     15: [False],
     16: [False],
     17: [False],
     18: [True],
     }

# True/False - Совместитель/Штатный, плюс отмечены дни и часы, когда преподаватели работать не могут
Teachers = {
      'Питеримова': [False],
      'Худякова': [False],
      'Васильева': [False], #, 16,17,19
      'Петрова': [False],#, 3,7,11,18
      'Салеева': [False],
      'Николаева': [False], #  , 1,10,30,32
      'Тимирева': [False],
      'Иванова': [False], #, 2,4,7,8,9,10,14,19,23,28,29,32
      'Никифорова': [False],
      'Иголкина': [False], #, 2, 8, 9, 14, 15, 31
      'Рыженкова': [True, 0,1,2,3,4,5,6,7,8,9,10,11,12,13, 16,21,22,23,24,25,26,27,28],
      'Колодин': [True,  0,1,2,3,4,5,6,7,8,9,10,11,12,13,21,22,23,24,25,26,27],
      'Филиппова': [False, 14,15,16,17,18,19,20,28,29,30,31,32,34],
      'Сизак': [False],
      'Колесник': [True, 14,15,16,17,18,19,20,31]
    }

Subjects = {
    # для деления на группы: класс не делится - 0, группы (иностранный) - 0.5, профильный предмет - 1, элективный курс - 1.5, классы занимаются вместе - 2

    # [0subject, 1class, 2teacher, 3audience, 4load, 5сложность, 6спаренность,
    # 7группы/профиль, 8занятость, 9номер_профиля, 10вес (определяет приоритет)]
    #
    0: ['Русский язык', 5, 'Петрова', 3, 5,    8, 0, 0, 0, 0, 0],
    1: ['Литература', 5, 'Петрова', 3, 3,   4, 0, 0, 0, 0, 0],
    2: ['Иностранный язык', 5, 'Васильева', 8, 3,   9, 0, 0, 0, 0, 0],
    3: ['Математика', 5, 'Николаева', 13, 5,   10, 0, 0, 0, 0, 0],
    5: ['История', 5, 'Филиппова', 16, 2,   5, 0, 0, 0, 0, 0],
    6: ['Обществознание', 5, 'Филиппова', 16, 1,   6, 0, 0, 0, 0, 0],
    7: ['География', 5, 'Никифорова', 4, 1,   7, 0, 0, 0, 0, 0],
    8: ['Биология', 5, 'Никифорова', 1, 1,   10, 0, 0, 0, 0, 0],
    9: ['Музыка', 5, 'Колесник', 15, 1,   2, 0, 0, 0, 0, 0],
    10: ['ИЗО', 5, 'Сизак', 17, 1,   3, 0, 0, 0, 0, 0],
    11: ['Технология', 5, 'Колесник', 15, 2,   4, 0, 0, 0, 0, 0],
    12: ['Физкультура', 5, 'Иванова', 18, 3,   3, 0, 0, 0, 0, 0],

    13: ['Русский язык', 6, 'Салеева', 14, 6,    12, 0, 0, 0, 0, 0],
    14: ['Литература', 6, 'Салеева', 14, 3,   6, 0, 0, 0, 0, 0],
    15: ['Иностранный язык', 6, 'Васильева', 8, 3,   11, 0, 0, 0, 0, 0],
    16: ['Математика', 6, 'Николаева', 13, 5,   13, 0, 0, 0, 0, 0],
    17: ['История', 6, 'Филиппова', 16, 2,   8, 0, 0, 0, 0, 0],
    18: ['Обществознание', 6, 'Филиппова', 16, 1,   9, 0, 0, 0, 0, 0],
    19: ['География', 6, 'Никифорова', 4, 1,   7, 0, 0, 0, 0, 0],
    20: ['Биология', 6, 'Никифорова', 1, 1,   8, 0, 0, 0, 0, 0],
    21: ['Музыка', 6, 'Колесник', 15, 1,   1, 0, 0, 0, 0, 0],
    22: ['ИЗО', 6, 'Сизак', 17, 1,   3, 0, 0, 0, 0, 0],
    23: ['Технология', 6, 'Колесник', 15, 2,   3, 0, 0, 0, 0, 0],
    24: ['Физкультура', 6, 'Иванова', 18, 3,   4, 0, 0, 0, 0, 0],

    25: ['Русский язык', 7, 'Салеева', 14, 4,    11, 0, 0, 0, 0, 0],
    26: ['Литература', 7, 'Салеева', 14, 2,   4, 0, 0, 0, 0, 0],
    27: ['Иностранный язык', 7, 'Питеримова', 6, 3,   10, 0, 0, 0, 0, 0],
    28: ['Алгебра', 7, 'Тимирева', 5, 3,   10, 0, 0, 0, 0, 0],
    29: ['Геометрия', 7, 'Тимирева', 5, 2,   12, 0, 0, 0, 0, 0],
    30: ['Информатика', 7, 'Колодин', 7, 1,   4, 0, 0, 0, 0, 0],
    31: ['История', 7, 'Филиппова', 16, 2,   6, 0, 0, 0, 0, 0],
    32: ['Обществознание', 7, 'Филиппова', 16, 1,   9, 0, 0, 0, 0, 0],
    33: ['География', 7, 'Никифорова', 4, 2,   6, 0, 0, 0, 0, 0],
    34: ['Биология', 7, 'Никифорова', 1, 2,   7, 0, 0, 0, 0, 0],
    35: ['Физика', 7, 'Иголкина', 2, 2,   8, 0, 0, 0, 0, 0],
    36: ['Музыка', 7, 'Колесник', 15, 1,   1, 0, 0, 0, 0, 0],
    37: ['ИЗО', 7, 'Сизак', 17, 1,   1, 0, 0, 0, 0, 0],
    38: ['Технология', 7, 'Колесник', 15, 1,   2, 0, 0, 0, 0, 0],
    39: ['Физкультура', 7, 'Иванова', 18, 3,   2, 0, 0, 0, 0, 0],
    40: ['ОБЖ', 7, 'Колодин', 7, 1,   3, 0, 0, 0, 0, 0],

    41: ['Русский язык', 8, 'Петрова', 3, 3,    7, 0, 0, 0, 0, 0],
    42: ['Литература', 8, 'Петрова', 3, 2,   4, 0, 0, 0, 0, 0],
    43: ['Иностранный язык', 8, 'Питеримова', 6, 3,   8, 0, 0, 0, 0, 0],
    44: ['Алгебра', 8, 'Николаева', 13, 3,   9, 0, 0, 0, 0, 0],
    45: ['Геометрия', 8, 'Николаева', 13, 2,   10, 0, 0, 0, 0, 0],
    46: ['Информатика', 8, 'Колодин', 7, 1,   7, 0, 0, 0, 0, 0],
    47: ['История', 8, 'Филиппова', 16, 2,   8, 0, 0, 0, 0, 0],
    48: ['Обществознание', 8, 'Филиппова', 16, 1,   5, 0, 0, 0, 0, 0],
    49: ['География', 8, 'Никифорова', 4, 2,   6, 0, 0, 0, 0, 0],
    50: ['Биология', 8, 'Никифорова', 1, 2,   7, 0, 0, 0, 0, 0],
    51: ['Химия', 8, 'Никифорова', 1, 2,   10, 0, 0, 0, 0, 0],
    52: ['Физика', 8, 'Иголкина', 2, 2,   9, 0, 0, 0, 0, 0],
    53: ['ИЗО', 8, 'Сизак', 17, 1,   3, 0, 0, 0, 0, 0],
    54: ['Технология', 8, 'Колесник', 15, 1,   1, 0, 0, 0, 0, 0],
    55: ['Черчение', 8, 'Иголкина', 2, 1,   5, 0, 0, 0, 0, 0],
    56: ['Физкультура', 8, 'Иванова', 18, 3,   2, 0, 0, 0, 0, 0],
    57: ['ОБЖ', 8, 'Колодин', 7, 1,   3, 0, 0, 0, 0, 0],

    58: ['Русский язык', 9, 'Салеева', 14, 2,    6, 0, 0, 0, 0, 0],
    # 59: ['Русский язык', 9, 'Салеева', 14, 1,    6, 0, 0, 0, 0, 0], #(гиа)
    60: ['Литература', 9, 'Салеева', 14, 3,   7, 0, 0, 0, 0, 0],
    61: ['Иностранный язык', 9, 'Питеримова', 6, 3,   9, 0, 0.5, 0, 0, 1000],
    62: ['Алгебра', 9, 'Тимирева', 5, 3,   7, 0, 0, 0, 0, 0],
    # 63: ['Алгебра', 9, 'Тимирева', 5, 1,   7, 0, 0, 0, 0, 0], #(гиа)
    64: ['Геометрия', 9, 'Тимирева', 5, 2,   8, 0, 0, 0, 0, 0],
    65: ['Информатика', 9, 'Колодин', 7, 2,   7, 0, 0.5, 0, 0, 0],
    66: ['История', 9, 'Рыженкова', 16, 2,   10, 0, 0, 0, 0, 0],
    67: ['Обществознание', 9, 'Рыженкова', 16, 1,   8, 0, 0, 0, 0, 0],
    68: ['География', 9, 'Никифорова', 4, 2,   5, 0, 0, 0, 0, 0],
    69: ['Биология', 9, 'Никифорова', 1, 2,   7, 0, 0, 0, 0, 0],
    70: ['Химия', 9, 'Никифорова', 1, 2,   12, 0, 0, 0, 0, 0],
    71: ['Физика', 9, 'Иголкина', 2, 2,   13, 0, 0, 0, 0, 0],
    72: ['Физика', 9, 'Иголкина', 2, 1,   13, 0, 0, 0, 0, 0], #(гиа)
    73: ['ИЗО', 9, 'Сизак', 17, 1,   2, 0, 0, 0, 0, 0],
    74: ['Физкультура', 9, 'Иванова', 18, 3,   2, 0, 0, 0, 0, 0],
    75: ['Технология', 9, 'Колесник', 15, 1,   4, 0, 0, 0, 0, 0],
    76: ['ОБЖ', 9, 'Худякова', 7, 1,   3, 0, 0.5, 0, 0, 0],
    #
    # # естественно(1)-гуманитарный(2) профиль
    77: ['Физика', 10, 'Иголкина', 2, 2,   12, 0, 0, 0, 0, 0],
    78: ['Литература', 10, 'Петрова', 3, 3,   8, 0, 0, 0, 0, 0],
    79: ['Иностранный язык', 10, 'Питеримова', 6, 3,   8, 0, 0, 0, 0, 0],
    80: ['История', 10, 'Рыженкова', 16, 2,   5, 0, 0, 0, 0, 0],
    81: ['Обществознание', 10, 'Рыженкова', 16, 2,   5, 0, 0, 0, 0, 0],
    82: ['Химия', 10, 'Никифорова', 1, 1,   11, 0, 0, 0, 0, 0],
    83: ['Физкультура', 10, 'Иванова', 18, 3,   1, 0, 0, 0, 0, 0],
    84: ['ОБЖ', 10, 'Худякова', 7, 1,   2, 0, 0, 0, 0, 0],
    85: ['Геометрия', 10, 'Тимирева', 5, 2,   11, 0, 0, 0, 0, 0],
    86: ['Алгебра', 10, 'Тимирева', 5, 2,   10, 0, 0, 0, 0, 0],
    87: ['Русский язык', 10, 'Петрова', 3, 1,    9, 0, 0, 0, 0, 0], #(егэ)
    88: ['Алгебра', 10, 'Тимирева', 5, 1,    10, 0, 0, 0, 0, 0], #(егэ)
    89: ['Русский язык', 10, 'Петрова', 3, 3, 9, 0, 1, 0, 2, 0],
    90: ['Биология', 10, 'Никифорова', 1, 3, 7, 0, 1, 0, 1, 0],
    91: ['Биология', 10, 'Никифорова', 1, 1, 7, 0, 0.8, 0, 1, 0],  # (элективный)
    92: ['Физика', 10, 'Иголкина', 2, 1, 12, 0, 0.8, 0, 1, 0], # (элективный курс)
    93: ['Информатика', 10, 'Колодин', 7, 1,   6, 0, 0, 0, 0, 0],
    94: ['География', 10, 'Иголкина', 4, 2,   3, 0, 0, 0, 0, 0], # (? или Никифорова)

    # # социально(3)-математический(4) профиль
    95: ['Физика', 11, 'Иголкина', 2, 2,   12, 0, 0, 0, 0, 0],
    96: ['Русский язык', 11, 'Петрова', 3, 1,    9, 0, 0, 0, 0, 0],
    97: ['Литература', 11, 'Петрова', 3, 3,   8, 0, 0, 0, 0, 0],
    98: ['Иностранный язык', 11, 'Питеримова', 6, 3,   8, 0, 0, 0, 0, 0],

    99: ['История', 11, 'Рыженкова', 16, 2,   5, 0, 0, 0, 0, 0],
    100: ['Химия', 11, 'Никифорова', 1, 1,   11, 0, 0, 0, 0, 0],
    101: ['Физкультура', 11, 'Иванова', 18, 3,   1, 0, 0, 0, 0, 0],
    102: ['ОБЖ', 11, 'Худякова', 7, 1,   2, 0, 0, 0, 0, 0],

    103: ['Алгебра', 11, 'Тимирева', 5, 3,   10, 0, 1, 0, 4, 0],
    104: ['Обществознание', 11, 'Рыженкова', 16, 3,   5, 0, 1, 0, 3, 0],
    105: ['Информатика', 11, 'Колодин', 7, 1,   6, 0, 0, 0, 0, 0],
    106: ['Биология', 11, 'Никифорова', 1, 1,   7, 0, 0, 0, 0, 0],

    107: ['Русский язык', 11, 'Петрова', 3, 1,    9, 0, 0, 0, 0, 0], # (егэ)
    108: ['Алгебра', 11, 'Тимирева', 5, 1,    10, 0, 0, 0, 0, 0], # (егэ)
    109: ['Русский язык', 11, 'Петрова', 3, 1,    9, 0, 0.8, 0, 0, 0], # (элективный)
    110: ['Физика', 11, 'Иголкина', 2, 1,   12, 0, 0.8, 0, 0, 0], # (элективный курс)
    111: ['Биология', 11, 'Никифорова', 1, 1,   7, 0, 0.8, 0, 0, 0], # (элективный курс)
    112: ['Алгебра', 11, 'Тимирева', 5, 3,   10, 0, 0, 0, 0, 0]

}

print('||||||||||||||Начало||||||||||||||||')
# Расстановка коэфициентов и упорядочивание предметов
Subjects = set_weight_and_sort(Subjects)

days = 5
max_hour = 7  # по санпин
hours_in_week = days*max_hour

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

    # ставит одиночным занятиям - один учитель/один предмет/один класс/две группы - удвоенную нагрузку - на каждую группу
    distribute_double_load(Subjects)

    # рассчитывает реальную нагрузку для таблицы запрещений
    calculate_the_load(Subjects)

    # количество параметров (для последующих действий)
    params_lenght = len(next (iter (Subjects.values())))

    # первоначальное заполнение сетки расписания единицами
    for h in range((hours_in_week)*len(Classes)):
        H[h] = 1


    # Таблицы запрещений
    args["week_hour_class"] = build_table_of_bans(Classes, 'c', week_hour_class)
    args["week_hour_teacher"] = build_table_of_bans(Teachers, 't', week_hour_teacher)
    args["week_hour_audience"] = build_table_of_bans(Audiences, 'a', week_hour_audience)



    #===================================================================

    # уменьшили часы, после частичной расстановки (у групповых предметов)
    less_hours = False


    counter = 0
    # расстановка предметов в сетку расписания
    for s in range(len(Subjects)):


        # параметры для групповых и профильных занятий (гр/пр, гр - групповой, пр - профильный)

        # если у гр/пр предмета есть, что поставить в ним на одно время
        single_lesson = False

        # если у гр/пр пары предметов совпадает нарузка
        load_is_equal = True

        # текущий предмет, который первоначально расставляем в сетку, имеет бОльшую нагрузку, чем найденный ему в пару (для пр)
        current_is_bigger = False

        # отвечает за удвоение нагрузки в случаях 1учитель/1предмет/1класс/2группы
        double = 1

        # индексы, которые требуется удалить, чтобы предмет мог стать только первым или последним уроком
        days_to_delete = []

        params = Subjects[list(Subjects)[s]]


        # если урок нуждается в расстановке - вперед
        if params[8] != 100:

            counter = counter+1
            found_lessons = []

            print('=======================================')
            print('Предмет №', counter)
            print('Текущий предмет: ', params[0], params[1], params[2], 'Нагрузка', params[4])

            # если предмет не общий
            if params[7] != 0:
                # надо найти ему что-то в пару, если есть (чтобы занять весь класс, а не его часть)
                found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal = find_a_pair(params,
                                                                                                               found_lessons,
                                                                                                               single_lesson,
                                                                                                               current_is_bigger,
                                                                                                               days_to_delete,
                                                                                                               load_is_equal)
            # запуск функции расстановки
            less_hours = go(params_lenght, found_lessons, current_is_bigger, params, double,
               single_lesson, week_hour_audience, week_hour_teacher,
               week_hour_class, days_to_delete, H, s, load_is_equal, less_hours)

        print('Закончили расстановку предмета')

    args['H'] = []
    args['H_teachers'] = []

    # для вывода стандартного расписания по класссам
    for v in H.values():
        if v != 1:
            if len(v) > params_lenght:  # определяем, один там предмет или нет
                args['H'].append(v[0]+'/'+v[params_lenght])
            else:
                args['H'].append(v[0])
        else:
            args['H'].append(v)

    # для вывода расписания по учителям
    for v in H.values():
        if v != 1:
            if len(v) > params_lenght:  # параметры добавляются по 10 штук
                args['H_teachers'].append(v[2]+'/'+v[params_lenght+2])
            else:
                args['H_teachers'].append(v[2])
        else:
            args['H_teachers'].append(v)


    # # обнуляем, чтобы можно было заново смотреть КОСЯК В ГРУППАх!!!
    # for subject in Subjects.values():
    #     subject[8] = 0

    return render_to_response("generate.html", args)

# ======================================================
# ======================================================
# ======================================================
# ----------------------functions-----------------------

# распределение нагрузки
def distribute_the_load(params_lenght, single_lesson, params,  week_hour_audience, week_hour_teacher, week_hour_class, found_lessons, days_to_delete, double, H, s,less_hours):
    free_index, num_class, num_audience, num_teacher = find_free_indexes(params_lenght,
                                                                         params,
                                                                         week_hour_audience,
                                                                         week_hour_class,
                                                                         week_hour_teacher,
                                                                         found_lessons)


    print('Получившиеся свободные индексы, на которые можно расставлять уроки')
    print(free_index)


    # удаляем все дни, кроме первого и последнего урока (для уроков без пары, если это групповой или профильный предмет)
    if single_lesson:
        for day in days_to_delete:
            if day in free_index:
                free_index.remove(day)
        print('Урок для части класса и в пару поставить не с кем, поэтому: ')
        print(free_index)

    # для большей устойчивости
    first_copy_free_index = copy.deepcopy(free_index)

    # пробуем выполнить нормы СанПиН
    free_index = sanpin(params, free_index)

    print('После функции СанПин')
    print(free_index)

    # если есть возможность, убираем спаренность
    if len(free_index) >= params[4]:
        free_index = remove_paired(free_index, num_class, H, s)
    print('После попытки убрать спаренность')
    print(free_index)

    if len(free_index) == 0:
        free_index = first_copy_free_index
        print('К сожалению, оптимизацию по СанПин и спаренности никак не выполнить')

    print('Итог:')
    print(free_index)

    # выбор индекса дня, куда будем ставить предмет в сетку H
    hour_cell = choice(free_index)  # hour_cell -- hour_subject
    print('В эту ячейку поставим текущую итерацию предмета', hour_cell)

    key_H = (hours_in_week)*(num_class)+hour_cell  # индекс ячейки в сетке распсиания H
    H[key_H] = list(Subjects[list(Subjects)[s]])

    if len(found_lessons) == params_lenght:
        H[key_H] = H[key_H] + found_lessons
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

# Найти еще групповые или профильные предметы
def find_a_pair(params, found_lessons,  single_lesson, current_is_bigger, days_to_delete, load_is_equal):

    # начинаем с 1 чтобы учесть и текущий предмет - должно быть вместе с ним парное количество (иначе будет обработка другая)
    count_of_lessons = 1

    # ищем такой же предмет, но который ведет другой учитель
    for lesson in range(len(Subjects)):

        # если проверяемый предмет еще не расставлен в сетку
        if Subjects[list(Subjects)[lesson]][8] != 100:

            # если это текущий класс
            if Subjects[list(Subjects)[lesson]][1] == params[1]:

                # ДЛЯ ГРУППОВЫХ ПРЕДМЕТОВ
                # и если для него также требуется деление на группы
                if Subjects[list(Subjects)[lesson]][7] == 0.5:
                    print('Это групповой предмет')

                    # учитель другой
                    if Subjects[list(Subjects)[lesson]][2] != params[2]:

                        # но если это текущий предмет добавь его в список
                        if Subjects[list(Subjects)[lesson]][0] == params[0]:
                            found_lessons.append(Subjects[list(Subjects)[lesson]])

                        # если это не текущий предмет
                        else:
                            # проверяем, нет ли у этого урока пары с таким же уроком, и если нет, тогда добавь его в список
                            if is_not_repeated_lessons(Subjects[list(Subjects)[lesson]]):
                                found_lessons.append(Subjects[list(Subjects)[lesson]])
                else:
                    # ДЛЯ ПРОФИЛЬНЫХ ПРЕДМЕТОВ
                    # если это тоже профильный предмет
                    if Subjects[list(Subjects)[lesson]][7] == 1:
                        print('Это профильный предмет')

                        # если это не тот же самый профиль (а другая половина класса задействована)
                        if Subjects[list(Subjects)[lesson]][9] != params[9]:
                                found_lessons.append(Subjects[list(Subjects)[lesson]])

    print('Нашли в пару этот предмет', found_lessons)

    if len(found_lessons) != 0:

        # этот говнокод нужно будет исправить :/
        found_lessons = found_lessons[0]
        count_of_lessons = 2
        current_is_bigger = False

        if found_lessons[4] != params[4]:
            load_is_equal = False

            # если еще остаются часы у найденного предмета, тогда нужно их убавить у него в исходных данных
            if params[4]-found_lessons[4] > 0:
                current_is_bigger = True

        print('Текущий имеет большую нагрузку?', current_is_bigger)

    # если текущий урок является групповым и пары для него нет,
    # тогда его можно будет поставить только первым и последним уроком, чтобы не было окна
    if count_of_lessons % 2 != 0:
        days_to_delete = [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31,32,33]
        single_lesson = True

    return found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal
#---------------------------------------------------------------

# Поиск подходящих часов для расстановки предмета в соотвествие с занятостью учителей, классов и кабинетоа
def find_free_indexes(params_lenght, params, week_hour_audience, week_hour_class, week_hour_teacher, found_lessons):
    temp = []
    count_of_classes = 1

    # если в найденных один предмет
    if len(found_lessons) == params_lenght:
        count_of_teachers = count_of_audience = 2
    else:
        count_of_teachers = count_of_audience = len(found_lessons)+1


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
            if len(found_lessons) == params_lenght:
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
            if len(found_lessons) == params_lenght:
                for l in range(1):
                    add_to_temp(temp, week_hour_audience, found_lessons, 3, num_audience, a_number, Audiences)
                break
            else:
                for l in range(len(found_lessons)):
                    add_to_temp(temp, week_hour_audience, found_lessons[last_lesson_number], 3, num_audience, a_number, Audiences)
                    last_lesson_number = last_lesson_number + 1
                break

    # ================================

    print('Матрица свободных часов: ', len(temp))
    for ind in range(len(temp)):
        print(temp[ind])

    # массив для подсчета результата логического перемножения
    r = []

    # транспонирование матрицы (удобнее логически перемножать)
    temp_t = list(zip(*temp))

    for i in range(len(temp_t)):
        if temp_t[i][0] & temp_t[i][1] & temp_t[i][2]:
            r.append(1)
        else:
            r.append(0)

    print('Результат логического перемножения матрицы:')
    print(r)

    # индексы тех ячеек в сетке, куда можно ставить текущее занятие (получаем из результирующего вектора)
    free_index = []

    for j in range(len(r)):
        if r[j] == 1:
            free_index.append(j)

    return free_index, num_class, num_audience, num_teacher
#---------------------------------------------------------------

# для добавления во временный массив
def add_to_temp(temp, week_hour_item, params, n, num_item, i_number, items):

    for i in range(len(items)):
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

    for_del_max = [1, 2, 3, 8, 9, 10, 15, 16, 17, 22, 23, 24, 29, 30, 31]  # уроки с наибольшей нагрузкой
    for_del_min = [0, 4, 5, 6, 7, 11, 12, 13, 14, 18, 19, 20, 21, 25, 26, 27, 28, 32, 33, 34]  # уроки с наименьшей нагрузкой

    # если урок относится к легким урокам
    if params[5] < 8:
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

    if len(free_index) == 0:
        print('Нормы СанПин не выполнить(')
        free_index = copy_free_index

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

            if len(free_index) == 0:
                free_index = copy_free_index

    return free_index
#---------------------------------------------------------------
# ставим пометку, о том, что урок расставлен или остались еще часы
def mark_lesson(params_lenght, found_lessons, load_is_equal, current_is_bigger, params, less_hours):

    # если предмет в найденных только один
    if len(found_lessons) == params_lenght:
        # print('-----')
        # print('len(found_lessons)', len(found_lessons))
        # print(load_is_equal)

        # если нагрузка у предметов равна, просто поставь отметку, чтобы их больше не трогать
        if load_is_equal:
            found_lessons[8] = 100
        else:
            # иначе проверяем у кого нагрузка больше, у текущего предмета или у найденного
            # если у текущего больше - тогда убираем найденный предмет, вся его нагрузка расставлена
            print(current_is_bigger)
            if current_is_bigger:
                found_lessons[8] = 100

            else:
                # уменьшаем нагрузку найденного предмета, оставляя только не расставленные часы
                found_lessons[4] = found_lessons[4]-params[4]
                less_hours = True
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
                    less_hours = True
                    # print('+')
                    # print('осталось расставить ', found_lessons[subject][4], ' часов')
                    # print('+')
    return less_hours
#-----------------------------------

# запускает расстановку нагрузки со всеми предварительными действиями
def go(params_lenght,
       found_lessons,
       current_is_bigger,
       params, double,
       single_lesson,
       week_hour_audience,
       week_hour_teacher,
       week_hour_class,
       days_to_delete,
       H, s, load_is_equal,
       less_hours):

    print('Запускается функция "go"')

    if less_hours == True:
        double = 1
        less_hours = False

    # учет нагрузки (сколько уроков расставить)
    if len(found_lessons) != 0:
        if current_is_bigger:
            limit = found_lessons[4]
        else:
            limit = params[4]
    else:
        limit = params[4]

    print('Количество расстановок - ', limit)

    # начинаем рассставлять в соотвествии с нагрузкой
    for load in range(limit):

        distribute_the_load(params_lenght,
                            single_lesson,
                            params,
                            week_hour_audience,
                            week_hour_teacher,
                            week_hour_class,
                            found_lessons,
                            days_to_delete,
                            double, H, s,
                            less_hours)
    less_hours = mark_lesson(params_lenght, found_lessons, load_is_equal, current_is_bigger, params, less_hours)

    # запустить функцию, чтоб дорасставлялись остальные часы, оставшиеся у текущего урока
    if len(found_lessons) != 0:
        if current_is_bigger:
            print('Так как текущий урок имеет бОльшую нагрузку, ищем новый в пару')
            params[4] = params[4]-found_lessons[4]
            less_hours = True
            single_lesson = True
            found_lessons = []
            if params[7] != 0:
                found_lessons, single_lesson, current_is_bigger, days_to_delete, load_is_equal = find_a_pair( params,
                                                                                                               found_lessons,
                                                                                                               single_lesson,
                                                                                                               current_is_bigger,
                                                                                                               days_to_delete,
                                                                                                               load_is_equal)

            # если урок найденный уже расставлен, а урок текущий еще не до конца - дорасставляем оставшиеся часы
            less_hours = go(params_lenght, found_lessons, current_is_bigger, params, double,
                   single_lesson, week_hour_audience, week_hour_teacher,
                   week_hour_class, days_to_delete, H, s, load_is_equal, less_hours)
        else:
            Subjects[list(Subjects)[s]][8] = 100

    return less_hours

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

# расставить удвоенною нагрузку там, где это нужно
def distribute_double_load(Subjects):
    print('У групповых предметов удваивается нагрузка')

    for subject in list(Subjects.values()):
        if subject[7] == 0.5 and is_not_repeated_lessons(subject):
            subject[4] = subject[4]*2

#-----------------------------------------

# для подсчета нагрузки
def calculate_the_load(Items):

    copy_of_Items = Items

    for sclass in list(Classes):

        load = 0
        list_group_load = []
        dict_profile_load = {}
        dont_use = []
        group_load = 0
        profile_load = 0
        elective_load = 0

        for item in list(copy_of_Items.values()):

            # считаем общие предметы
            if item[1] == sclass and item[7] == 0:
                load = load + item[4]

            # ищем групповые
            if item[1] == sclass and item[7] == 0.5:
                list_group_load.append(item[4])
                print(list_group_load)

            # считаем элективные предметы
            if item[1] == sclass and item[7] == 0.8:
                elective_load = elective_load + item[4]

            # ищем профильные
            if item[1] == sclass and item[7] == 1:

                # если словарь пуст просто добавить
                if len(dict_profile_load) == 0:
                    dict_profile_load[item[9]] = item[4]
                    dont_use.append(item)
                else:
                    flag = False

                    # иначе перебираем все значения, если находим такой же профиль - увеличиваем у него значение
                    # если такого профиля нет, добавляем этот профиль в словарь (для определения этого и нужен флаг)
                    if item not in dont_use:
                        for profile in list(dict_profile_load):
                            if profile == item[9]:
                                dict_profile_load[profile] += item[4]
                                dont_use.append(item)
                                flag = True
                    if not flag:
                        dict_profile_load[item[9]] = item[4]

        # профильная нагрузка
        if len(dict_profile_load) != 0:
            profile_load = max(dict_profile_load.values())
        else:
            profile_load = 0

        # групповая нагрузка
        if len(list_group_load) == 0:
            group_load = 0
        else:

            if len(list_group_load) == 1:
                group_load = list_group_load[0]
            else:
                if sum(list_group_load) % 2 == 0:
                    print('sum')
                    if len(list_group_load) != 2:
                        group_load = sum(list_group_load)//2
                        if group_load % 2 != 0:
                            group_load = max(list_group_load)
                    else:
                        group_load = max(list_group_load)
                else:

                    # плохо работает
                    for l1 in list_group_load:
                        if l1 in list_group_load:
                            if list_group_load.count(l1) % 2 == 0:
                                group_load = group_load+l1
                                for i in range(list_group_load.count(l1)):
                                    list_group_load.remove(l1)
                                print('ffffffffff1', list_group_load, group_load)
                            if list_group_load.count(l1) > 2 and list_group_load.count(l1) % 2 != 0:
                                group_load = group_load+l1
                                for i in range(0,1):
                                    list_group_load.remove(l1)
                                print('ffffffffff2', list_group_load, group_load)

                    # если что-то еще осталось
                    if len(list_group_load) != 0:
                        if len(list_group_load) == 1:
                            group_load = group_load+list_group_load[0]
                        else:
                            # сумма оставшейся нагрузки без максимальной
                            w = (sum(list_group_load) - max(list_group_load))
                            group_load = group_load + w + (max(list_group_load) - w)*2
                    print(group_load, 'grpuo')


        full_load = load + profile_load + group_load + elective_load

        Classes[sclass] = full_load
        print('Класс: ', sclass, 'Нагрузка общих предметов: ', load,
                                 'Групповая: ', group_load,
                                 'Профильная: ', profile_load,
                                 'Элективная: ', elective_load,
                                 'Суммарная нагрузка: ', full_load)

# проверяет, есть ли у группового предмета текущего класса такой же парный предмет. Например - два алнглийских, но учителя разные
def is_not_repeated_lessons(lesson):
    for subject in list(Subjects.values()):
        if subject[0] == lesson[0] and subject[2] != lesson[2] and subject[1] == lesson[1]:
            return False
    return True


# построить таблицы запрещений (name - c, t, a - classes, teachers, audiences)
def build_table_of_bans(Items, name, week_hour_item):

    ban = []

    for i in range(len(Items)):
        if name == "t" or name == "a":
            ban = Items[list(Items)[i]]

            # убираем ненужные здесь параметры True/False
            if ban != [] and (ban[0] == True or ban[0] == False):
                del ban[0]

        week_hour_item.append([])
        if len(ban) == 0:

            # обработка для классов
            if name == 'c':
                for hour in range(1, hours_in_week+1):
                    if list(Items)[i]<7:
                        if hour%7 == 0:
                            week_hour_item[i].append(0)
                        else:
                            week_hour_item[i].append(1)
                    if list(Items)[i]>=7:
                        week_hour_item[i].append(1)

                # распределение максимальной нагрузки по санпин для классов
                if sum(week_hour_item[i]) > Items[list(Items)[i]]:
                    d = sum(week_hour_item[i]) - Items[list(Items)[i]]
                    if d == 1:
                        if int(list(Items)[i]) < 7:
                            ch = [5, 12, 26, 33]
                            r = choice(ch)
                            ch.remove(r)
                            week_hour_item[i][r] = 0
                        else:
                            week_hour_item[i][randrange(6, hours_in_week, max_hour)] = 0
                    if d>1:
                        if int(list(Items)[i]) < 7:
                            ch = [5, 12, 26, 33]
                        else:
                            ch = [6, 13, 27, 34]  # пн, вт, чт, пт
                        ch2 = [5, 12, 26, 33]
                        for j in range(0, d):
                            if len(ch) != 0:
                                r = choice(ch)
                                ch.remove(r)
                            else:
                                r = choice(ch2)
                                ch2.remove(r)
                            week_hour_item[i][r] = 0

            # для учителей и аудиторий
            else:
                for hour in range(0, hours_in_week):
                    week_hour_item[i].append(1)
        else:
            for hour in range(0, hours_in_week):
                if hour in ban:
                    week_hour_item[i].append(0)
                else:
                    week_hour_item[i].append(1)

    return week_hour_item



