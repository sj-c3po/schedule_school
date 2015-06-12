from django.conf.urls import patterns, url

urlpatterns = patterns('',

 # ex: /polls/5/
 #    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),

    url(r'^add_subject/?', 'schedule.views.add_subject'),
    url(r'^archive/?', 'schedule.views.archive'),
    url(r'^new/delete_object/?', 'schedule.views.delete_object'),
    url(r'^new/save_ban_days/?', 'schedule.views.save_ban_days'),
    url(r'^new/?', 'schedule.views.new'),
    url(r'^main/?', 'schedule.views.show_main'),
    url(r'^opened_schedule/?', 'schedule.views.open_schedule'),
    url(r'^login/?', 'schedule.views.login'),
    url(r'^logout/?', 'schedule.views.logout'),
    url(r'^schedule_detailed/?', 'schedule.views.schedule_detailed'),
    # url(r'^schedule/?', 'schedule.views.schedule'),
    url(r'^schedule/?', 'schedule.algorithm_4.views.schedule'), # это поменяли для отображения в нужном окне
    url(r'^save_schedule?', 'schedule.views.save_schedule'),
    # url(r'^generate/?', 'schedule.algorithm_1.views.generate'), # это самый первый, где работают основные функции
    # url(r'^generate/?', 'schedule.algorithm_2.views.generate'), # это я хотела сделать "историю"
    # url(r'^generate/?', 'schedule.algorithm_3.views.generate'), # тут работает расстановка, но выталкивания еще нет, поэтому некотрые часы вываливаются
    # url(r'^generate/?', 'schedule.algorithm_4.views.generate'), # это попробую сделать "выталкивание"
    url(r'^', 'schedule.views.show_auth'),           # должно быть внизу, потому что смотрится построчно

    # все переадресовывается c schedule/...
)
