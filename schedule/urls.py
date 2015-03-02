from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'schedule_school.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^new/teachers/?', 'schedule.views.add_teachers'),
    url(r'^new/classes/?', 'schedule.views.add_classes'),
    url(r'^new/classrooms/?', 'schedule.views.add_classrooms'),
    url(r'^new/lessons/?', 'schedule.views.add_lessons'),
    url(r'^new/example/?', 'schedule.views.example_steps'),
    url(r'^new/?', 'schedule.views.new'),
    url(r'^main/?', 'schedule.views.show_main'),
    url(r'^login/?', 'schedule.views.login'),
    url(r'^logout/?', 'schedule.views.logout'),
    url(r'^schedule_detailed/?', 'schedule.views.schedule_detailed'),
    url(r'^schedule/?', 'schedule.views.schedule'),
    url(r'^', 'schedule.views.show_auth'),           # должно быть внизу, потому что смотрится построчно

    # все переадресовывается c schedule/...
)
