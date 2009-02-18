# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db import models
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType

from commons import (get_form_class, change_foreing_key, apply_filters,
                     special_procesing)

@login_required
def save_ajax(request):
    if request.POST:
        try:
            post = request.POST.copy()
            application_form = post.get('application_form')
            form = post.get('form', None)
            content_type_id = post.get('content_type_id')
            obj_id = post.get('id')
            field = post.get('field')
            value = simplejson.loads(post.get('value'))
            filters = simplejson.loads(post.get('filters','[]'))
            is_cmsutils = post.get('is_cmsutils', False)
            form_class = get_form_class(form, content_type_id)
            model_class = form_class._meta.model
            contenttype = ContentType.objects.get(id=content_type_id)
            assert contenttype.model_class() is model_class # check for hacker attack by changing POST
            obj = get_object_or_404(model_class,id=obj_id)


            new_data = change_foreing_key(obj)
            if isinstance(form_class.base_fields[field], ModelMultipleChoiceField):
                new_data[field] = value.split(',')
            else:
                new_data[field] = value

            form_obj = form_class(data=new_data, instance=obj)
            if form_obj.is_valid():
                current_language = request.session.get('django_language',
                                                       settings.LANGUAGE_CODE)
                obj = form_obj.save(current_language)
                value = getattr(obj, field)
                value = special_procesing(form_obj[field], value)
                value = apply_filters(value, filters)
                json_dict = json_encode({'errors':False, 'value': value})
            else:
                python_dict = dict(form_obj.errors)
                python_dict['errors'] = True
                json_dict = json_encode(dict(python_dict))

        except: # very scary!!!!
            json_dict = simplejson.dumps({'errors':True})

        return HttpResponse(json_dict,mimetype='application/json')

def json_encode(data, ensure_ascii=False):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has 
    problems with some models).
    """
    def _any(data):
        ret = None
        if isinstance(data, list):
            ret = _list(data)
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        else:
            try:
                ret = data.__unicode__()
            except:
                ret = data
        return ret

    def _model(data):
        return data.__unicode__()

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return simplejson.dumps(ret, cls=DateTimeAwareJSONEncoder, ensure_ascii=ensure_ascii)