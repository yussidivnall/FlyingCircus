from django.conf.urls import patterns, include, url
from django.conf import settings
#from imdb_training.views import *
from video_training.views import *
urlpatterns = patterns('',
    url(r'^$',start_page),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/volcan/Desktop/development/FlyingCircus/WebServer/test2'}),
    )
