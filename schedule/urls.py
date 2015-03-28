from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/teachers/?', 'schedule.views.teachers'),
    url(r'^new/classes/?', 'schedule.views.classes'),
    url(r'^new/classrooms/?', 'schedule.views.classrooms'),
    url(r'^new/?', 'schedule.views.new'),
    url(r'^main/?', 'schedule.views.show_main'),
    url(r'^login/?', 'schedule.views.login'),
    url(r'^logout/?', 'schedule.views.logout'),
    url(r'^processing_data/?', 'schedule.views.processing_data'),
    url(r'^schedule_detailed/?', 'schedule.views.schedule_detailed'),
    url(r'^schedule/?', 'schedule.views.schedule'),
    url(r'^', 'schedule.views.show_auth'),           # должно быть внизу, потому что смотрится построчно

    # все переадресовывается c schedule/...
)
