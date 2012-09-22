# -*- coding: utf-8 -*-

# django imports
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView

# app import
from test_fk.models import *

urlpatterns = patterns(
    'test_fk.views',
    (r'(?P<pk>\d+)/$', login_required(DetailView.as_view(
        model=Company,
        ))),
    (r'^$', TemplateView.as_view(
        template_name="test_fk/nothinghere.html",
    )),
)
