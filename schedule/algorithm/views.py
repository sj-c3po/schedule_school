from django.shortcuts import render_to_response, render
from random import *

# T = ['Иванова', 'Шматова', 'Королев', 'Градусова', 'Питеримова', 'Соболев', 'Веселова', 'Тюрина']
# A = [12, 13, 14, 25, 26, 27, 30, 31]
# C = [5, 6, 7, 8, 9, 10, 11] # классы

C = {5: 29,
     6: 30,
     7: 32,
     8: 33,
     9: 33,
     10: 34,
     11: 34}

T = {
        'Иванова': [5],
        'Шматова': [],
        'Королев': [14, 15, 16, 17, 18, 19, 20, 21],
        'Градусова': [],
        'Питеримова': [],
        'Соболев': [27, 28],
        'Веселова': []
    }

A = {12: [8, 4, 6],
     13: [],
     14: [],
     25: [],
     26: [12, 35, 15],
     27: [],
     30: []}

S = {1: ['Физкультура', 5, 'Иванова', 12, 3],  # [t, c, a, load] (класс_id, учитель_id, аудитория_id, недельная нагрузка)
     2: ['Физкультура', 6, 'Иванова', 12, 3],
     3: ['Физкультура', 11, 'Иванова', 12, 3],
     4: ['Информатика', 10, 'Соболев', 25, 2],
     5: ['Информатика', 11, 'Королев', 25, 2],
     6: ['История', 8, 'Шматова', 30, 2],
     7: ['Обществознание', 8, 'Шматова', 30, 2],
     8: ['Русский', 7, 'Иванова', 14, 4],
     9: ['Математика', 9, 'Веселова', 13, 4],
     10: ['Английский', 6, 'Питеримова', 26, 3],
     11: ['География', 7, 'Градусова', 27, 1],
}


days = 5
max_hour = 7  # по санпин
hours_in_week = days*max_hour


def generate(request):
    args = {}
    args['c'] = list(C)
    args['t'] = list(T)
    args['a'] = list(A)
    week_hour_class = []  # матрица week-hours-classes
    week_hour_teacher = []  # матрица week-hours-teachers
    week_hour_audience = []  # матрица week-hours-audience
    args['range'] = range(hours_in_week)  # для вывода таблицы
    H = {}  # сетка расписания


    # первоначальное заполнение сетки расписания
    for h in range((hours_in_week)*len(C)):
        H[h] = 1
    print(len(H))


    # таблица запрещений для классов
    for c in range(len(C)):
        week_hour_class.append([])
        for hour in range(1, hours_in_week+1):
            if list(C)[c]<7:
                if hour%7 == 0:
                    week_hour_class[c].append(0)
                else:
                    week_hour_class[c].append(1)
            if list(C)[c]>=7:
                week_hour_class[c].append(1)


        # распределение максимальной нагрузки по санпин
        # print('start')
        # print(sum(week_hour_class[c]))

        if sum(week_hour_class[c]) > C[list(C)[c]]:
            d = sum(week_hour_class[c]) - C[list(C)[c]]
            # print(str(d)+' d')
            if d == 1:
                if int(list(C)[c]) < 7:
                    # print(str(list(C)[c])+' klass1')
                    week_hour_class[c][randrange(5, hours_in_week, max_hour)] = 0
                else:
                    # print(str(list(C)[c])+' klass2')
                    week_hour_class[c][randrange(6, hours_in_week, max_hour)] = 0
            if d>1:
                ch = [6, 13, 27, 34] # пн, вт, чт, пт
                for j in range(1, d+1):
                    # print(str(list(C)[c])+' klass3')
                    r = choice(ch)
                    ch.remove(r)
                    week_hour_class[c][r] = 0
        # print('sum' + str(sum(week_hour_class[c])))
        # print('=========end==========')
    args["week_hour_class"] = week_hour_class


    #таблица запрещений для учителей
    for t in range(len(T)):
        print(list(T)[t])
        ban = T[list(T)[t]]
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
    for a in range(len(A)):
        print(list(A)[a])
        ban = A[list(A)[a]]
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



    # расстановка предметов в сетку расписания
    for s in range(len(S)):
        temp = []
        params = S[list(S)[s]]
        # print(params)
        # print('---------')

        # добавляем класс во временный массив
        num_class = 1
        for c in range(len(C)):
            if list(C)[c] == params[1]:
                temp.append(week_hour_class[c])
                break
            else:
                num_class = num_class+1

        # добавляем учителя
        num_teacher = 1
        for t in range(len(T)):
            if list(T)[t] == params[2]:
                temp.append(week_hour_teacher[t])
                break
            else:
                num_teacher = num_teacher+1

        # добавляем кабинет
        num_audience = 1
        for a in range(len(A)):
            if list(A)[a] == params[3]:
                temp.append(week_hour_teacher[a])
                break
            else:
                num_audience = num_audience+1

        # num_audience, num_teacher, num_class нужны для расстановки в сетку расписания (номер строки)


        # print(temp)
        r = []

        # транспонирование матрицы (удобнее логически перемножать)
        temp_t = list(zip(*temp))
        for i in range(len(temp_t)):

            # print(temp_t[i])
            # print('this', temp_t[i][0] & temp_t[i][1] & temp_t[i][2])

            if temp_t[i][0] & temp_t[i][1] & temp_t[i][2]:
                r.append(1)
            else:
                r.append(0)


        # а сюда нужно вбахать все проверки, чтобы r максимально сузился

        # индексы тех ячеек в сетке, куда можно ставить текущее занятие
        free_index = []

        for j in range(len(r)):
            if r[j] == 1:
                free_index.append(j)

        # print(free_index)

        # выбор индекса дня, куда будем ставить предмет в сетку H
        hs = choice(free_index)  # hs -- hour_subject
        # print(hs, 'hs')


        # print((hours_in_week)*(num_class-1), 'this is')
        keyH = (hours_in_week)*(num_class-1)+hs
        # print('--------')
        # print(num_class-1, 'num_class-1')
        # print(hs, 'hs')
        # print(keyH, 'keyH')

        # print(S[list(S)[s]], 'hhhh')
        H[keyH] = S[list(S)[s]]
        # print(H)


        week_hour_class[num_class-1][hs] = 0
        week_hour_teacher[num_teacher-1][hs] = 0
        week_hour_audience[num_audience-1][hs] = 0



    args['H'] = []

    # print('======')
    # print(H.values())
    # print(len(H), 'len(H)')
    # print(width-1, 'width-1')
    # print(len(C), 'len(C)')


    for v in H.values():
        if v!=1:
            args['H'].append(v[0])
        else:
            args['H'].append(v)

    return render_to_response("generate.html", args)



