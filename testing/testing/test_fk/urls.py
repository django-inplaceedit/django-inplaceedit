# -*- coding: utf-8 -*-

# django imports
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # Django 1.5
    from django.conf.urls import patterns, url

from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView

# app import
from testing.test_fk.models import Company


urlpatterns = patterns(
    'test_fk.views',
    (r'(?P<pk>\d+)/$', login_required(DetailView.as_view(
        model=Company,
    ))),
    (r'^$', TemplateView.as_view(
        template_name="test_fk/nothinghere.html",
    )),
)
