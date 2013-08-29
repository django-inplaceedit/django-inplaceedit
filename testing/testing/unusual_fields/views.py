# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from testing.unusual_fields.models import UnusualModel


def unusual_index(request):
    return render_to_response('unusual_fields/index.html',
                              {'unusual_objs': UnusualModel.objects.all()},
                              context_instance=RequestContext(request))


def unusual_edit(request, unusual_id):
    unusual_obj = get_object_or_404(UnusualModel, pk=unusual_id)
    return render_to_response('unusual_fields/edit.html',
                              {'unusual_obj': unusual_obj},
                              context_instance=RequestContext(request))
