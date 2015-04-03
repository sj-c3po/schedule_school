from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from schedule.models import *
import json

# Страница добавления
def new(request):
    args = {}
    if request.user.is_authenticated():
        args['username'] = request.user.get_username()
        args['classes'] = School_class.objects.all()
        args['subjects'] = Subject.objects.all()
        args['common_rel'] = CommonRel.objects.all()
        # args['common_rel_distinct_teacher'] = CommonRel.objects.all().distinct()
        # print(args['common_rel_distinct_teacher'])

        # c = Locate.objects.filter(state='AZ').values('city').order_by().distinct()

        args['teachers'] = Teacher.objects.all()
        args['staff_types'] = Staff_type.objects.all()

        # post работает плохо(
        if request.method == "POST":
            changes = request.POST.dict()

            keys = list(changes)
            i = 0
            k = 0
            db_subject = 0
            db_class = 0
            db_newval = 0
            for key in keys:
                if key == 'changes[%s][subject]' % i:
                    db_subject = changes[key]
                if key == 'changes[%s][sclass]' % i:
                    db_class = changes[key]
                if key == 'changes[%s][newval]' % i:
                    db_newval = changes[key]
                    # if db_newval == '':
                print('Нуы')

                k = k + 1
                if k % 3 == 0:
                    c = CommonRel.objects.get(sclass=School_class.objects.filter(class_name=db_class),
                                              subject=Subject.objects.filter(subject_name=db_subject))
                    if c != None:

                        c.subject_max_load = db_newval
                        c.save()
                    else:
                        print('else')
                        # c = CommonRel(sclass=School_class.objects.filter(class_name=db_class),
                        #               subject=Subject.objects.filter(subject_name=db_subject))
                        # c.save()
                        # c2 = CommonRel(sclass=4, subject=2, cabinet=2, teacher=1, subject_max_load=66, difficulty_level=1)
                        # c2.save()
    #
    # sclass = models.ForeignKey(School_class, verbose_name='Класс')
    # subject = models.ForeignKey(Subject, verbose_name='Предмет')
    # cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет')
    # teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
    # subject_max_load = models.IntegerField('Максимальная недельная нагрузка по предмету')
    # difficulty_level = models.Inte
    #                 i = i + 1


        return render_to_response('new.html', args)
    else:
        args['login_error'] = 'Вы не авторизованы!'
        return render_to_response('auth.html', args)


def login(request):
    args = {}
    if request.method == "POST":
        user_login = request.POST.get('login', '') # возьми логин, иначе присвой "пусто"
        user_password = request.POST.get('password', '') # возьми логин, иначе присвой "пусто"
        user = auth.authenticate(username=user_login, password=user_password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/main')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render_to_response('auth.html', args)
    else:
        return render(request, 'auth.html', args)


       # user = User.objects.create_user(user_login, None, user_password) - строка для регистрации пользователя


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


def schedule(request):
    args = {}
    args['username'] = request.user.get_username()
    args['schedule'] = 1
    return render_to_response('schedule.html', args)


def schedule_detailed(request):
    args = {}
    args['username'] = request.user.get_username()
    args['schedule'] = 1
    return render_to_response('schedule_detailed.html', args)


def show_auth(request):
    if request.user.is_authenticated():
        return redirect('/main')
    else:
        return render_to_response('auth.html')


def show_main(request):
    args = {}
    if request.user.is_authenticated():
        args['username'] = request.user.get_username()
        return render_to_response('main.html', args)
    else:
        args['login_error'] = 'Вы не авторизованы!'
        return render_to_response('auth.html', args)



def processing_data(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.POST)
        print('jdhgj '+data)