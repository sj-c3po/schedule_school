from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from schedule.models import *
# import numpy as np

# Страница добавления
def new(request):
    args = {}
    if request.user.is_authenticated():
        args['username'] = request.user.get_username()
        args['classes'] = School_class.objects.all()
        args['subjects'] = Subject.objects.all()
        args['common_rel'] = CommonRel.objects.all()
        args['teachers'] = Teacher.objects.all()
        args['staff_types'] = Staff_type.objects.all()
        # args['class_counter'] = 0
        args['len_common_rel'] = len(args['common_rel'])
        obj_not_ex = False

        if request.method == "POST":
            changes = request.POST

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
                k = k + 1

                if k % 3 == 0:
                    try:
                        c = CommonRel.objects.get(sclass=School_class.objects.filter(id=db_class),
                                                  subject=Subject.objects.filter(id=db_subject))
                        if db_newval == '':
                            c.subject_max_load = 0
                        else:
                            c.subject_max_load = db_newval
                        c.save()
                        break
                    except ObjectDoesNotExist:
                        obj_not_ex = True


                    if (obj_not_ex):
                        print('Здесь надо бы создать новый объект в базе')

        return render_to_response('new.html', args)
    else:
        args['login_error'] = 'Вы не авторизованы!'
        return render_to_response('auth.html', args)

def delete_object(request):
    args = {}
    if request.user.is_authenticated():
        if request.method == "POST" and request.is_ajax():
            delete_id = request.POST
            print(delete_id)
            # not working
            # for id in delete_id:
            #     print(delete_id[id])

    return render_to_response('new.html', args)


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



def add_subject(request):
    if request.method == "POST" and request.is_ajax():
        classes_id = request.POST.getlist('classes[]')
        weekload = request.POST.getlist('weekload[]')
        new_subject = list(request.POST.values())[2]

        print(type(classes_id))
        print(type(weekload))
        print(new_subject)

        arr_classes_id = [int(c) for c in classes_id.split(',')]
        arr_weekload = [int(w) for w in weekload.split(',')]

        print(arr_classes_id)
        print(arr_weekload)


# myarray = np.asarray(mylist)

    # example_list = [int(k) for k in example_string.split(',')]
    # print(example_list)

    return HttpResponseRedirect("/new")
    # return render_to_response('new.html')