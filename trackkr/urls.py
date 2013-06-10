from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    (r'^$', 'webui.views.index'),
    (r'^dashboard.html$', 'webui.views.dashboard'),
    (r'^login.html$', 'webui.views.log_in'),
    (r'^logout.html$', 'webui.views.log_out'),
    (r'^api/recentpos.json$', 'api.views.recentpos'),
    (r'^api/units/(?P<imei>[0-9]+).json$', 'api.views.lastpos'),
    (r'^api/units.json', 'api.views.units'),
    (r'^units.html$', 'webui.views.units'),
    (r'^units/add.html$', 'webui.views.unit_add'),
    (r'^units/(?P<imei>[0-9]+).html$', 'webui.views.unit'),
    (r'^units/delete/(?P<imei>[0-9]+).html$', 'webui.views.unit_delete'),
)
