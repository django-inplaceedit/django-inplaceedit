# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from testing.multimediaresources.models import Resource


def multimediaresources_index(request):
    return render_to_response('multimediaresources/index.html',
                              {'resources': Resource.objects.all()},
                              context_instance=RequestContext(request))


def multimediaresources_edit(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render_to_response('multimediaresources/edit.html',
                              {'resource': resource},
                              context_instance=RequestContext(request))
