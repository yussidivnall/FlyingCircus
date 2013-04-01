from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
 from django.contrib import admin
 admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test3.views.home', name='home'),
    # url(r'^test3/', include('test3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^image_training/',include('image_training.urls',namespace='image_training')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/volcan/Desktop/development/FlyingCircus/WebServer/media','show_indexes':True}),
    )
