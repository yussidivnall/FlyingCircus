from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^training_tools/', include('training_tools.urls',namespace='training_tools')),

    url(r'^imdb_training/',include('imdb_training.urls',namespace='imdb_training')),
    url(r'^video_training/',include('video_training.urls',namespace='video_training')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/volcan/Desktop/development/FlyingCircus/WebServer/media','show_indexes':True}),
    )
