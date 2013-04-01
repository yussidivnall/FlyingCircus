from django.conf.urls import patterns, include, url
from django.conf import settings
from imdb_training.views import *
urlpatterns = patterns('',
    url(r'^$',start_page),
    url(r'^search/$',search_page),
    url(r'^result/$', results_page),
    url(r'^actor/$', actor_page),
    url(r'^update_positives/$', update_positives),
    url(r'^train_all/$', train_all_page),
    url(r'^test_image/$', test_image),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/volcan/Desktop/development/FlyingCircus/WebServer/test2'}),
    )
