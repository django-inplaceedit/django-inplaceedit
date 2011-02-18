# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('multimediaresources.views',
   url(r'^$', 'index'),
   )
