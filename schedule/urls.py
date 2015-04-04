from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^new/delete_object/?', 'schedule.views.delete_object'),
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
