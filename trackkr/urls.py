from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    (r'^$', 'webui.views.index'),
    (r'^dashboard.html$', 'webui.views.dashboard'),
    (r'^login.html$', 'webui.views.log_in'),
    (r'^logout.html$', 'webui.views.log_out'),
    (r'^units.html$', 'webui.views.units'),
)
