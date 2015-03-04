from django.shortcuts import render, render_to_response, redirect
from django.template.loader import get_template
from django.contrib import auth
import json

def add_teachers(request):
    args = {}
    if request.method == "POST":
        args['count'] = request.POST['t_count']
        args['num'] = 1
        if not args['count'].isdigit():
            args['error'] = 'Ошибка ввода числа'
            return render_to_response('add_teachers.html', args)
        else:
            args['count'] = range(1, int(args['count'])+1)
            return render_to_response('add_teachers.html', args)
    else:
        return render_to_response('add_teachers.html')

def add_classes(request):
    args = {}
    args['class_number'] = [5, 6, 7, 8, 9, 10, 11]
    args['subjects'] = [1]
    if request.is_ajax():
         if request.method == "POST":
            args['data'] = json.loads(request.POST['data']); # from json to object
            print(args['data'])
            return render_to_response('add_classes.html', args)
    else:
        return render_to_response('add_classes.html', args)

def add_lessons(request):
    print("Уроки")
    return render_to_response('add_lessons.html')

def add_classrooms(request):
    print("Кабинеты")
    return render_to_response('add_classrooms.html')

def example_steps(request):
    return render_to_response('example.html')

# Страница добавления
def new(request):
    args = {}
    args['class_number'] = [5, 6, 7, 8, 9, 10, 11]
    args['alphabet'] = ['а','б','в','г','д','е','ж','з','и','к','л','м','н','о','п','р','с','т','у','ф','х'] #,'ц','ч','ш','щ','э','ю','я'
    args['username'] = request.user.get_username()
    return render_to_response('new.html', args)


def login(request):
    args = {}
    if request.method == "POST":
        user_login = request.POST.get('login', '') # возьми логин, иначе присвой "пусто"
        user_password = request.POST.get('password', '') # возьми логин, иначе присвой "пусто"
        user = auth.authenticate(username=user_login, password=user_password)
        # print(user.username, '\n' + user.password) - отладка
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
    return render_to_response('auth.html')

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
    username = request.user.get_username()
    return render_to_response('main.html', {'username': username})

