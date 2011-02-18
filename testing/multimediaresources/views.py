# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from multimediaresources.models import Resource, TypeResource


def index(request):
    return render_to_response('multimediaresources/index.html',
                              {'resources': Resource.objects.all(),
                               'types': TypeResource.objects.all()},
                              context_instance=RequestContext(request))
