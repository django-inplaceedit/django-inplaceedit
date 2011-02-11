# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import simplejson

from inplaceeditform.commons import (get_dict_from_obj, apply_filters,
                                     get_adaptor_class)


@login_required
def save_ajax(request):
    if not request.method == 'POST':
        return HttpResponse(simplejson.dumps({'errors': 'It is not a POST request'}),
                            mimetype='application/json')
    adaptor = _get_adaptor(request, 'POST')
    if not adaptor:
        return HttpResponse(simplejson.dumps({'errors': 'Params insufficient'}),
                            mimetype='application/json')
    value = simplejson.loads(request.POST.get('value'))
    new_data = get_dict_from_obj(adaptor.obj)
    form_class = adaptor.get_form_class()
    field_name = adaptor.field_name

    form = form_class(data=new_data, instance=adaptor.obj)
    try:
        value_edit = adaptor.get_value_editor(value)
        value_edit_with_filter = apply_filters(value_edit, adaptor.filters_to_edit)
        new_data[field_name] = value_edit_with_filter
        if form.is_valid():
            adaptor.save(value_edit_with_filter)
            return HttpResponse(simplejson.dumps({'errors': False,
                                            'value': adaptor.render_value()}),
                                mimetype='application/json')
        return HttpResponse(simplejson.dumps({'errors': form.errors}), mimetype='application/json')
    except ValidationError, error:
        message_i18n = ', '.join([u"%s" % m for m in error.messages])
        return HttpResponse(simplejson.dumps({'errors': message_i18n}), mimetype='application/json')


@login_required
def get_field(request):
    if not request.method == 'GET':
        return HttpResponse(simplejson.dumps({'errors': 'It is not a GET request'}),
                            mimetype='application/json')
    adaptor = _get_adaptor(request, 'GET')
    if not adaptor:
        return HttpResponse(simplejson.dumps({'errors': 'Params insufficient'}),
                            mimetype='application/json')

    field_render = adaptor.render_field()
    field_media_render = adaptor.render_media_field()
    return HttpResponse(simplejson.dumps({'field_render': field_render,
                                          'field_media_render': field_media_render}),
                                        mimetype='application/json')


def _get_adaptor(request, method='GET'):
    request_params = getattr(request, method)
    field_name = request_params.get('field_name', None)
    obj_id = request_params.get('obj_id', None)

    app_label = request_params.get('app_label', None)
    module_name = request_params.get('module_name', None)

    if not field_name or not obj_id or not app_label and module_name:
        return None

    contenttype = ContentType.objects.get(app_label=app_label,
                                          model=module_name)

    model_class = contenttype.model_class()
    obj = get_object_or_404(model_class,
                            pk=obj_id)
    adaptor = request_params.get('adaptor', None)
    class_adaptor = get_adaptor_class(adaptor, obj, field_name)

    filters_to_show = request_params.get('filters_to_show', None)

    kwargs = _convert_params_in_config(request_params, ('field_name',
                                                        'obj_id',
                                                        'app_label',
                                                        'module_name',
                                                        'filters_to_show',
                                                        'adaptor'))
    config = class_adaptor.get_config(**kwargs)
    adaptor_field = class_adaptor(request, obj, field_name,
                                               filters_to_show,
                                               config)
    return adaptor_field


def _convert_params_in_config(request_params, exclude_params=None):
    exclude_params = exclude_params or []
    config = {}
    options_widget = {}
    for key, value in request_params.items():
        if key not in exclude_params:
            if key.startswith('__widget_'):
                key = key.replace('__widget_', '')
                options_widget[key] = value
            else:
                config[str(key)] = value
    config['widget_options'] = options_widget
    return config
