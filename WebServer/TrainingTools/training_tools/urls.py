
from django.conf.urls import patterns, include, url
from django.conf import settings
from training_tools.views import start_page
urlpatterns = patterns('',
    url(r'^$',start_page, name='home'),
)
