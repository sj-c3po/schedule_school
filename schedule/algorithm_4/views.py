from django.shortcuts import render_to_response
from random import *
from schedule.models import *
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
                        subject[10] = 85
                    else:
                        if subject[7] == 0.8:
                            subject[10] = 70
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
                if subject[1] == 11:
                    subject[10] = subject[10]*10
                if subject[1] == 10:
                    subject[10] = subject[10]*9
                if subject[1] == 9:
                    subject[10] = subject[10]*8
                if subject[1] == 5:
                    subject[10] = subject[10]*7
                if subject[1] == 6:
                    subject[10] = subject[10]*4
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

# расставить удвоенною нагрузку там, где это нужно
def distribute_double_load(Subjects):
    print('У групповых предметов удваивается нагрузка')

    for subject in list(Subjects.values()):
        if subject[7] == 0.5 and is_not_repeated_lessons(subject):
            subject[4] = subject[4]*2

# проверяет, есть ли у группового предмета текущего класса такой же парный предмет. Например - два алнглийских, но учителя разные
def is_not_repeated_lessons(lesson):
    for subject in list(Subjects.values()):
        if subject[0] == lesson[0] and subject[2] != lesson[2] and subject[1] == lesson[1]:
            return False
    return True
# ------------------------------------------------------------------------------------


monday = [0, 1, 2, 3, 4, 5, 6]
tuesday = [7, 8, 9, 10, 11, 12, 13]
wednesday = [14, 15, 16, 17, 18, 19, 20]
thursday = [21, 22, 23, 24, 25, 26, 27]
friday = [28, 29, 30, 31, 32, 33, 34]

Classes = {}
Audiences = {}
Teachers = {}
Subjects = {}

# Заполнение Classes параллелями и их максимальной нагрузкой
Classes_query = School_class.objects.all().values()
for cl in Classes_query:
    Classes[cl['parallel']] = cl['class_max_load']

# Заполнение словаря кабинетов. True - специфичный (спортзал, компьютерный класс и т.п.)
Audiences_query = Cabinet.objects.all().values()
for aud in Audiences_query:
    Audiences[int(aud['cabinet_number'])] = [aud['specific']]
print(Audiences)

# Заполнение словаря учителей. True - совместитель
Teachers_query = Teacher.objects.all().values()
for t in Teachers_query:
    if t['ban_hours'] != None:
        Teachers[t['last_name']+t['first_name'][0]+t['middle_name'][0]] = [t['staff_type']]
        for char in t['ban_hours'].split(','):
            Teachers[t['last_name']+t['first_name'][0]+t['middle_name'][0]].append(int(char))
    else:
        Teachers[t['last_name']+t['first_name'][0]+t['middle_name'][0]] = [t['staff_type']]


print(Teachers)


# Заполнение учебным планом
Subjects_query = CommonRel.objects.all().values()
print(Subjects_query)
s_id = 0
for s in Subjects_query:

    subj = str(Subject.objects.get(id=s['subject_id']))
    cl = School_class.objects.get(id=s['sclass_id']).parallel
    t = Teacher.objects.get(id=s['teacher_id']).last_name+\
        Teacher.objects.get(id=s['teacher_id']).first_name[0]+\
        Teacher.objects.get(id=s['teacher_id']).middle_name[0]
    aud = int(Cabinet.objects.get(id=s['cabinet_id']).cabinet_number)

    # деление класса
    division = 0
    cprofile = 0
    # print(s['division_class_id'], type(s['division_class_id']))
    if s['division_class_id'] == 1:  # электив
        division = 0.8
    if s['division_class_id'] == 2:  # групповой
        division = 0.5
    if s['division_class_id'] == 3:  # профиль
        division = 1
        cprofile = s['profile_id']


    Subjects[s_id] = [subj, cl, t, aud, int(s['subject_max_load']), s['difficulty_level'], 0, division, 0, cprofile, 0]
    # print(Subjects[s_id])
    s_id = s_id + 1

# exit(0)

    # [0subject, 1class, 2teacher, 3audience, 4load, 5сложность, 6спаренность,
    # 7группы/профиль/электив, 8занятость, 9номер_профиля, 10вес (определяет приоритет)]

    # 0: ['Русский язык', 5, 'Петрова', 3, 5,    8, 0, 0, 0, 0, 0],

free_for_ban_hours_Classes = {
                 5: [5, 12, 19, 26, 33],
                 6: [5, 12, 19, 26, 33],
                 7: [6, 13, 20, 27, 34],
                 8: [6, 13, 20, 27, 34],
                 9: [6, 13, 20, 27, 34],
                 10: [6, 13, 20, 27, 34],
                 11: [6, 13, 20, 27, 34, 5, 12, 19, 26, 33]
                 }

print('||||||||||||||Начало||||||||||||||||')

# для комбинаторного подсчета нужно знать первоначальные нагрузки (они изменяются в процессе, поэтому надо записать сразу)
loads = {}
for key, value in Subjects.items():
    loads[key] = value[4]

days = 5
max_hour = 7  # по санпин
hours_in_week = days*max_hour
args = {}

# def generate(request):  # , Teachers, Audiences, Subjects, free_for_ban_hours_Classes так потом надо юудет с JS
def schedule(request):  # , Teachers, Audiences, Subjects, free_for_ban_hours_Classes так потом надо юудет с JS
    args['c'] = list(Classes)
    args['t'] = list(Teachers)
    args['a'] = list(Audiences)
    week_hour_class = []  # матрица week-hours-classes
    week_hour_teacher = []  # матрица week-hours-teachers
    week_hour_audience = []  # матрица week-hours-audience
    args['range'] = range(hours_in_week)  # для вывода таблицы
    H = {}  # сетка расписания
    not_distributed = {}

    global Subjects, Audiences, Teachers, free_for_ban_hours_Classes

    # это необходимо для корректного обновления, все данные возвращаются к первоначальным параметрам
    copy_Subjects = copy.deepcopy(Subjects)
    copy_Teachers = copy.deepcopy(Teachers)
    copy_Audiences = copy.deepcopy(Audiences)
    deep_copy_free_for_ban_hours_Classes = copy.deepcopy(free_for_ban_hours_Classes)

    # print('+++==++==++==++==++')
    # print(copy_Teachers)
    # # print(copy_Audiences)
    # print('+++==++==++==++==++')

    # Расстановка коэфициентов и упорядочивание предметов
    Subjects = set_weight_and_sort(Subjects)

    # увеличивает исходную нагрузку групповых предметов в два раза
    distribute_double_load(Subjects)

    for key, values in Subjects.items():
        print(key, values)

    # рассчитывает реальную нагрузку для таблицы запрещений
    calculate_the_load(Subjects)

    # количество параметров (для последующих действий)
    params_lenght = len(next (iter (Subjects.values())))

    # первоначальное заполнение сетки расписания единицами
    for h in range((hours_in_week)*len(Classes)):
        H[h] = 1


    # Таблицы запрещений
    args["week_hour_class"] = build_table_of_bans(Classes, 'c', week_hour_class)
    print("Эти часы еще можно запретить у классов", free_for_ban_hours_Classes)

    args["week_hour_teacher"] = build_table_of_bans(Teachers, 't', week_hour_teacher)
    args["week_hour_audience"] = build_table_of_bans(Audiences, 'a', week_hour_audience)

    # это может быть пригодится для смены запрета последних уроков
    print('Таблица занятости классов')
    for row in args["week_hour_class"]:
        for n, value in enumerate(row):
            if value == 0:
                row[n] = 2
        print(row)

    print('Таблица занятости учителей')
    for row in args["week_hour_teacher"]:
        print(row)

    print('Таблица занятости аудиторий')
    for row in args["week_hour_audience"]:
        print(row)

    #===================================================================

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

        # индексы, которые требуется удалить, чтобы предмет мог стать только первым или последним уроком
        days_to_delete = []

        limit = 0
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
            print('-----go-----')

            go_is_finished = False
            # сколько нагрузки уже расставлено
            load_placed = 0

            load_placed, go_is_finished = go(params_lenght, found_lessons, current_is_bigger, params,
                                                single_lesson, week_hour_audience, week_hour_teacher,
                                                week_hour_class, days_to_delete, H, s, load_is_equal,
                                                limit, load_placed, not_distributed, go_is_finished,
                                                copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)
            print('-----end go-----')

        print('Закончили расстановку предмета')

    # формируем вывод расписания
    args['Schedule'] = {}
    args['H'] = []
    args['H_teachers'] = []

    # для вывода стандартного расписания класс/предмет
    for k, v in H.items():
        if v != 1:
            args['Schedule'][k] = v
            if len(v) > params_lenght:  # определяем, один там предмет или нет
                args['H'].append(v[0]+'/'+v[params_lenght])
            else:
                args['H'].append(v[0])
        else:
            # args['H'].append(v)
            args['H'].append('-')

    # для вывода расписания класс/учитель
    for v in H.values():
        if v != 1:
            if len(v) > params_lenght:  # параметры добавляются по 10 штук
                args['H_teachers'].append(v[2]+'/'+v[params_lenght+2])
            else:
                # args['H_teachers'].append(v[2])
                args['H_teachers'].append(v[2])
        else:
            # args['H_teachers'].append(v)
            args['H_teachers'].append('-')


    # обнуляем, чтобы можно было заново смотреть КОСЯК В ГРУППАх!!!
    for subject in Subjects.values():
        subject[8] = 0

    print('Нерасставленных', len(not_distributed))
    for item in not_distributed.items():
        print(item)

    # Subjects, Teachers, Audiences, free_for_ban_hours_Classes = reset_data(copy_Subjects, copy_Teachers,
    #                                                                        copy_Audiences, deep_copy_free_for_ban_hours_Classes)

    # print(Teachers)
    # print(copy_Teachers)
    #
    # print('1+=+=+')
    # for key, value in Subjects.items():
    #     print(value)
    # print('1+=+=+')

    Subjects = copy_Subjects
    Teachers = copy_Teachers
    Audiences = copy_Audiences
    free_for_ban_hours_Classes = deep_copy_free_for_ban_hours_Classes

    # print('2+=+=+')
    # for key, value in Subjects.items():
    #     print(value)
    # print('2+=+=+')

    # print(copy_Teachers)
    # print(copy_Audiences)/


    args['username'] = request.user.get_username()
    args['schedule'] = 1

    # return render_to_response("generate.html", args)
    return render_to_response("schedule.html", args)

# ======================================================
# ======================================================
# ======================================================
# ----------------------functions-----------------------


# распределение нагрузки
def distribute_the_load(params_lenght, single_lesson,
                        params,  week_hour_audience,
                        week_hour_teacher, week_hour_class,
                        found_lessons, days_to_delete, H, s,
                        current_is_bigger, load_is_equal, load_placed, not_distributed, go_is_finished,
                        copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):

    print('load_placed', load_placed, go_is_finished)

    if not go_is_finished:

        free_index, num_class, num_audience, num_teacher, go_is_finished, temp = find_free_indexes(params_lenght,
                                                                             params,
                                                                             week_hour_audience,
                                                                             week_hour_class,
                                                                             week_hour_teacher,
                                                                             found_lessons,
                                                                             current_is_bigger,
                                                                             single_lesson, days_to_delete,
                                                                             H, s, load_is_equal, load_placed, not_distributed, go_is_finished,
                                                                             copy_Subjects, copy_Teachers, copy_Audiences,
                                                                             deep_copy_free_for_ban_hours_Classes)


        print('После первого go load_placed =', load_placed)
        if free_index != None:

            print('Получившиеся свободные индексы, на которые можно расставлять уроки')
            print(free_index)

            # ТУТ КОСЯЧИТ. НАДО БЫ ЧТО-ТО СДЕЛАТЬ С СИНГЛ ЛЕССОН, ИНАЧЕ ИНОГДА ВЫВАЛИВАЮТСЯ
            # удаляем все дни, кроме первого и последнего урока (для уроков без пары, если это групповой или профильный предмет)
            if single_lesson:

                copy_free = copy.deepcopy(free_index)

                if params[7] == 0.8:
                    print(free_index)

                for day in days_to_delete:
                    if day in free_index:
                        free_index.remove(day)
                print('Урок для части класса и в пару поставить не с кем, поэтому: ')
                print(free_index)

                if params[7] == 0.8 and free_index == []:
                    free_index = find_index_for_last_subject(temp, copy_free)

                    print('Опять косяк с элективом')
                    exit(0)


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
                week_hour_audience[index_audience][hour_cell] = 0
                # week_hour_audience[index_audience][hour_cell] = params[1]

            load_placed = load_placed + 1
            print('Столько нагрузки уже расставили -', load_placed)
        else:
            print('end load placed', load_placed, go_is_finished)
            if not go_is_finished:
                # если частично расставилось, оставить только нерасставленный час
                if load_placed < params[4]:
                    params[4] = params[4]-load_placed
                not_distributed[s] = Subjects[list(Subjects)[s]]
                print('ЗАКОНЧИЛИ')

    return load_placed
#---------------------------------------------------------------
def find_index_for_last_subject(temp, copy_free):

    before_twos = []

    for key, value in temp[0]:
        print(key, value)
        if value == 2 and temp[0][key-1] == 1:
                before_twos.append(key-1)

    print('before_twos', before_twos)


# выбираем и проверяем новую комбинацию индексов
def pick_new_used_indexes(branches, of, record):

    # списываем комбинацию, которая не работает
    print('До', branches[record])

    # не надо 100500 раз добавлять одну и ту же комбинацию
    if sorted(branches[record]['used']) not in sorted(branches[record]['not_fit']):
        branches[record]['not_fit'].append(branches[record]['used'])

    branches[record]['free_index'].extend(branches[record]['used'])
    branches[record]['used'] = []
    print('После', branches[record])

    for n in range(of):
        pick = choice(branches[record]['free_index'])
        branches[record]['used'].append(pick)
        branches[record]['free_index'].remove(pick)

    print('Теперь пробуем это', branches[record])

    # смотрим, чтоб комбинация не повторялась, иначе - рекурсия
    for elem in branches[record]['not_fit']:
        if sorted(branches[record]['used']) == sorted(elem):
            pick_new_used_indexes(branches, of, record)

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
                    else:
                        if Subjects[list(Subjects)[lesson]][7] == 0.8:
                            print('Это элективный предмет')



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
def find_free_indexes(params_lenght, params, week_hour_audience, week_hour_class, week_hour_teacher, found_lessons,
                      current_is_bigger, single_lesson, days_to_delete, H, s, load_is_equal, load_placed, not_distributed, go_is_finished,
                      copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):

    print('Запускается find_free_indexes')

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

    # если нет пересечений, нужно проверить, есть ли нулевые строки в матрице (запускаем функцию)
    if sum(r) == 0:
        free_index, load_placed, go_is_finished = place_with_new_ban(temp, params, week_hour_class,
                     params_lenght, found_lessons, current_is_bigger,
                     single_lesson, week_hour_audience, week_hour_teacher,
                     days_to_delete, H, s, load_is_equal, load_placed, not_distributed, go_is_finished,
                     copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)
    else:
        # индексы тех ячеек в сетке, куда можно ставить текущее занятие (получаем из результирующего вектора)
        free_index = []

        for j in range(len(r)):
            if r[j] == 1:
                free_index.append(j)

    return free_index, num_class, num_audience, num_teacher, go_is_finished, temp
#---------------------------------------------------------------

# доставляем нагрузку, меняя местами запрещенный час с другим
def place_with_new_ban(temp, params, week_hour_class,
                       params_lenght, found_lessons, current_is_bigger,
                       single_lesson, week_hour_audience, week_hour_teacher,
                       days_to_delete, H, s, load_is_equal, load_placed, not_distributed, go_is_finished,
                       copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):

    print('Запускается place_with_new_ban')

    row_is_zero = False

    for row in temp:
        if sum(row) == 0:
            row_is_zero = True

    if row_is_zero:
        print('Неверное количество часов у учителей либо у классов.'
              'Нужно перепроверить часы у преподавателя или у класса')
    else:
        # надо брать какие-то другие индексы
        print('Нужно брать другие индексы')

        further = True
        # пока для обычных уроков (смотрим какие свободные часы учителя)
        i = 0
        indexes = []
        if len(temp) == 3:
            for char in temp[1]:
                if char == 1:
                    indexes.append(i)
                i = i+1
            print('Свободные часы учителя', indexes)

            print('на что можно поменять', free_for_ban_hours_Classes[params[1]])

            if free_for_ban_hours_Classes[params[1]] != []:
                for h in free_for_ban_hours_Classes[params[1]]:
                    for hour in range(len(temp[0])):
                        if hour == h:
                            print('h', h, 'hour', hour, 'temp[0][hour]', temp[0][hour])
                            if temp[0][hour] == 0:
                                free_for_ban_hours_Classes[params[1]].remove(h)
                                print('Удалили', h)
                        # if temp[0][hour] == 2 and firstly:
                        #     indexes_with_twos.append(hour)

                indexes_with_twos = []
                for hour in range(len(temp[0])):
                    if temp[0][hour] == 2:
                        indexes_with_twos.append(hour)

                c = list(set(indexes) & set(free_for_ban_hours_Classes[params[1]]))
                print('Пересечение:', c)

                print('Было week_hour_class')
                for row in args["week_hour_class"]:
                    print(row)

                further = preparing_to_change_index_places(indexes, params, week_hour_class, further, load_placed, indexes_with_twos, temp,
                                                           copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)

                print('Стало week_hour_class')
                for row in args["week_hour_class"]:
                    print(row)
            else:
                further = False

        if len(temp) == 5:
            print('Длина матрицы равна 5')
            # reset_data(copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)
            exit(0)

        print(further)
        # выталкивания пока нет, поэтому флаг
        if further:
            limit = params[4]-load_placed
            if limit > 3:
                print('Столько раз доставить:', limit)
                # Subjects, Teachers, Audiences, free_for_ban_hours_Classes = reset_data(copy_Subjects, copy_Teachers,
                #                                                                            copy_Audiences, deep_copy_free_for_ban_hours_Classes)
                exit(0)
            else:
                print('-----further_go-----')
                load_placed, go_is_finished = go(params_lenght, found_lessons, current_is_bigger, params,
                                                single_lesson, week_hour_audience, week_hour_teacher,
                                                week_hour_class, days_to_delete, H, s, load_is_equal,
                                                limit, load_placed, not_distributed, go_is_finished,
                                                copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)
                print('-----end further_go-----')

    free_index = None
    return free_index, load_placed, go_is_finished

# подготовка к смене дня запрета для конкретного индекса
def preparing_to_change_index_places(indexes, params, week_hour_class, further, load_placed, indexes_with_twos, temp,
                                     copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):

    print('Запускается preparing_to_change_index_places')

    need_indexes = []  # индексы, которые в конце концов останутся для оставшейся нагрузки (они будут наиболее подходящими)
    last_hours_of_day = [5,6,12,13,19,20,26,27,33,34]
    cut_indexes = []  # здесь будут только те индексы, которые приходятся на последние часы в день

    print('Столько индексов было у учителя свободных', indexes)

    for i in indexes:
        if i in last_hours_of_day:
            cut_indexes.append(i)

    print('Индексы, которые приходятся на последние в день', cut_indexes)
    print('Индексы класса, где стоят двойки', indexes_with_twos)

    # те индексы, которые совпадают у учителя и ученика. У учеников там двойки, а у учителя - возможность провести урок
    inter_indexes = list(set(cut_indexes) & set(indexes_with_twos))
    print('Желательно взять эти индексы', inter_indexes)

    if inter_indexes != [] and len(inter_indexes) >= (params[4]-load_placed):
        for_choice = inter_indexes
        print('Отсюда будем набирать новые индексы', for_choice)

        for times in range(params[4]-load_placed):
            i = choice(for_choice)
            need_indexes.append(i)
            for_choice.remove(i)
        print('Хватает ровно. А столько индексов нам нужно', need_indexes)

    else:
        for_choice = cut_indexes
        print('Отсюда будем набирать новые индексы', for_choice)

        for times in range(len(for_choice)):
            i = choice(for_choice)
            need_indexes.append(i)
            for_choice.remove(i)
        print('Ровно не хватает. А столько индексов нам нужно', params[4]-load_placed)
        # Subjects, Teachers, Audiences, free_for_ban_hours_Classes = reset_data(copy_Subjects, copy_Teachers,
        #                                                                                    copy_Audiences, deep_copy_free_for_ban_hours_Classes)
        # exit(0)

    # если есть индексы для расстановки
    if need_indexes != []:

        # нахожу индекс, который надо поменять местами
        for index in need_indexes:

            copy_free_for_ban_hours_Classes = copy.deepcopy(free_for_ban_hours_Classes[params[1]])

            if len(free_for_ban_hours_Classes[params[1]]) != 0:
                further = changing_index_places(index, params, week_hour_class, further, copy_free_for_ban_hours_Classes)

            # если ни на что поменять нельзя, тогда проверяем, где у класса свободные индексы
            else:
                find_index_for_help(params, indexes_with_twos, index, temp)

                further = changing_index_places(index, params, week_hour_class, further, copy_free_for_ban_hours_Classes)
                print('preparing_to_change_index_places', further)
    return further

# ищем индексы, которые можно заменить с 1 на 2 (т.е. закрыть их, чтоб найти свободный час)
def find_index_for_help(params, indexes_with_twos, index, temp):
    day1 = []
    day2 = []

    print('Начался while')
    ahtung = 0
    while day1 == day2 and ahtung < 30:
        added_hour = choice(indexes_with_twos)-1
        day1 = day_of_week(added_hour)
        day2 = day_of_week(index)
        print(day1, day2)
        print('Длительность цикла', ahtung)
        ahtung = ahtung + 1

    if ahtung >= 30:
        print('Цикл while слишком разошелся(')
        exit(0)

    # if temp[0][added_hour+1] == 2:
    free_for_ban_hours_Classes[params[1]].append(added_hour)
    # else:
    #     print('Рядом справа не двойка, нельзя брать', added_hour)
    #     find_index_for_help(params, indexes_with_twos, index, temp)
    print('Добавили в помощь', free_for_ban_hours_Classes[params[1]])


# смена дня
def changing_index_places(index, params, week_hour_class, further, copy_free_for_ban_hours_Classes):

    print('Запускается changing_index_places')
    print('Индексы, свободные для замены', copy_free_for_ban_hours_Classes)

    if copy_free_for_ban_hours_Classes != []:
        index_for_changing = choice(copy_free_for_ban_hours_Classes)
        print('Этот индекс заменим на 2', index_for_changing)

        # ищу индекс класса
        for i in range(len(free_for_ban_hours_Classes)):
            if list(free_for_ban_hours_Classes)[i] == params[1]:
                founded_index = i

        further = changing(week_hour_class, founded_index, index_for_changing, index, params, copy_free_for_ban_hours_Classes, further)
    else:
        further = False
    print('changing_index_places', further)
    return further

def changing(week_hour_class, founded_index, index_for_changing, index, params, copy_free_for_ban_hours_Classes, further):
    # и в таблице у этого класса меняю значения местами, где свободно, а где нет
    if week_hour_class[founded_index][index_for_changing] != 0:
        week_hour_class[founded_index][index_for_changing] = 2
        week_hour_class[founded_index][index] = 1
        free_for_ban_hours_Classes[params[1]].remove(index_for_changing)
        # free_for_ban_hours_Classes[params[1]].append(index) # ??? нужно ли так делать
        print('Поменяли этот с 2 на 1', index)
    else:
        print("Там уже занято")
        print(copy_free_for_ban_hours_Classes)
        copy_free_for_ban_hours_Classes.remove(index_for_changing)
        print(copy_free_for_ban_hours_Classes)

        if copy_free_for_ban_hours_Classes != []:
            print('Вызвали рекурсию')
            further = changing_index_places(index, params, week_hour_class, further, copy_free_for_ban_hours_Classes)
        else:
            print('Больше ничего не осталось, предмет не расставлен')
            further = False
    print('changing', further)
    return further

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
def mark_lesson(params_lenght, found_lessons, load_is_equal, current_is_bigger, params):
    print('Запускается mark lesson')
    # если предмет в найденных только один
    if len(found_lessons) == params_lenght:
        print('mark if')

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
    else:

        print('mark else')
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
#-----------------------------------

# запускает расстановку нагрузки со всеми предварительными действиями
def go(params_lenght,
       found_lessons,
       current_is_bigger,
       params,
       single_lesson,
       week_hour_audience,
       week_hour_teacher,
       week_hour_class,
       days_to_delete,
       H, s, load_is_equal,
       limit, load_placed, not_distributed, go_is_finished,
       copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):

    print('>>>>Запускается функция "go", уже расставили', load_placed)
    print(go_is_finished)

    # учет нагрузки (сколько уроков расставить)
    if limit == 0:
        if len(found_lessons) != 0:
            if current_is_bigger:
                limit = found_lessons[4]
            else:
                limit = params[4]
        else:
            limit = params[4]

    print('Количество расстановок - ', limit)

    cn = 0
    # начинаем рассставлять в соотвествии с нагрузко
    for load in range(limit):
        cn = cn+1
        print('расстановка', cn)
        print('---до---', load_placed)
        load_placed = distribute_the_load(params_lenght,
                            single_lesson,
                            params,
                            week_hour_audience,
                            week_hour_teacher,
                            week_hour_class,
                            found_lessons,
                            days_to_delete,
                            H, s,
                            current_is_bigger, load_is_equal,
                            load_placed, not_distributed, go_is_finished,
                            copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)

        print('---после---', load_placed)

    print('Значение go_is_finished', go_is_finished)

    mark_lesson(params_lenght, found_lessons, load_is_equal, current_is_bigger, params)

    # запустить функцию, чтоб дорасставлялись остальные часы, оставшиеся у текущего урока
    if len(found_lessons) != 0:
        if current_is_bigger:
            print('Так как текущий урок имеет бОльшую нагрузку, ищем новый в пару')
            params[4] = params[4]-found_lessons[4]
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
            print('-----go-----')
            load_placed, go_is_finished = go(params_lenght, found_lessons, current_is_bigger, params,
                                                single_lesson, week_hour_audience, week_hour_teacher,
                                                week_hour_class, days_to_delete, H, s, load_is_equal,
                                                limit, load_placed, not_distributed, go_is_finished,
                                                copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes)
            print('-----end go-----')
        else:
            print('Предмет расставлен')
            Subjects[list(Subjects)[s]][8] = 100

    if  load_placed == params[4]:
        go_is_finished = True

    print('return load', load_placed, go_is_finished)
    return load_placed, go_is_finished

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
                print(item)
                list_group_load.append(item[4])

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
                        if len(list_group_load) != 2:
                            group_load = sum(list_group_load)//2
                            if group_load % 2 != 0:
                                group_load = max(list_group_load)
                        else:
                            group_load = max(list_group_load)
                    else:

                        # # плохо работает
                        # for l1 in list_group_load:
                        #     if l1 in list_group_load:
                        #         if list_group_load.count(l1) % 2 == 0:
                        #             group_load = group_load+l1
                        #             for i in range(list_group_load.count(l1)):
                        #                 list_group_load.remove(l1)
                        #             # print('ffffffffff1', list_group_load, group_load)
                        #         if list_group_load.count(l1) > 2 and list_group_load.count(l1) % 2 != 0:
                        #             group_load = group_load+l1
                        #             for i in range(0,1):
                        #                 list_group_load.remove(l1)
                        #             # print('ffffffffff2', list_group_load, group_load)

                        # если что-то еще осталось
                        if len(list_group_load) != 0:
                            if len(list_group_load) == 1:
                                group_load = group_load+list_group_load[0]
                            else:
                                # сумма оставшейся нагрузки без максимальной
                                w = (sum(list_group_load) - max(list_group_load))
                                group_load = group_load + w + (max(list_group_load) - w)*2
                        # print(group_load, 'grpuo')


        full_load = load + profile_load + group_load + elective_load

        Classes[sclass] = full_load
        print('Класс: ', sclass, 'Нагрузка общих предметов: ', load,
                                 'Групповая: ', group_load,
                                 'Профильная: ', profile_load,
                                 'Элективная: ', elective_load,
                                 'Суммарная нагрузка: ', full_load)


# построить таблицы запрещений (name - c, t, a - classes, teachers, audiences)
def build_table_of_bans(Items, name, week_hour_item):

    ban = []

    print('++++++++++++++==============+++++++++')
    print(Items)

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
                    # здесь убираем седьмые уроки у 5 и 6 класса - их там вообще нельзя проводить
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
                        else:
                            r = randrange(6, hours_in_week, max_hour)
                        week_hour_item[i][r] = 0

                        # сюда записываем часы, которые запретили  проводить
                        free_for_ban_hours_Classes[list(Items)[i]].remove(r)

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

                            # сюда записываем часы, которые запретили  проводить
                            free_for_ban_hours_Classes[list(Items)[i]].remove(r)

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

    print(Items)

    return week_hour_item

# # сброс данных в первоначальное состояние
# def reset_data(copy_Subjects, copy_Teachers, copy_Audiences, deep_copy_free_for_ban_hours_Classes):
#     Subjects = copy_Subjects
#     Teachers = copy_Teachers
#     Audiences = copy_Audiences
#     free_for_ban_hours_Classes = deep_copy_free_for_ban_hours_Classes
#     return Subjects, Teachers, Audiences, free_for_ban_hours_Classes


