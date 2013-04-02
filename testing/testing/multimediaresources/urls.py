# -*- coding: utf-8 -*-

try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # Django 1.5
    from django.conf.urls import patterns, url


urlpatterns = patterns('testing.multimediaresources.views',
                       url(r'^$', 'index'),
)
