# -*- coding: utf-8 -*-

from django.template import Library, Variable
from django.conf import settings
from django.utils import simplejson
from django.utils.translation import ugettext_lazy
from django.utils.translation import get_language
from django.contrib.contenttypes.models import ContentType

from inplaceeditform.commons import (get_form_class, apply_filters,
                                     special_procesing)

register = Library()

def inplace_media(context):
    return context.update({
            'user': context['request'].user,
            'MEDIA_URL': context.get('MEDIA_URL', settings.MEDIA_URL),
            'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
    })
register.inclusion_tag("inplace_media.html", takes_context=True)(inplace_media)


def inplace_edit(context, obj, expression, form='', expression2=None):
    content_type_id = ContentType.objects.get_for_model(obj.__class__).id
    form_class = get_form_class(form, content_type_id)
    prefix = '%s_%s'%(content_type_id, obj.id)
    form_obj = form_class(instance=obj, prefix=prefix)
    tokens = expression.split('|')
    field, filters = tokens[0], tokens[1:]
    field_obj = form_obj[field]

    request = context['request']
    current_language = get_language()
    value = getattr(obj, field, '-----')
    value = special_procesing(field_obj, value)

    value = apply_filters(value, filters)

    empty_value = value.strip() == u''

    if expression2:
        tokens = expression2.split('|')
        field2, filters2 = tokens[0], tokens[1:]
        value2 = Variable(field2).resolve(context)
        value2 = apply_filters(value2, filters2)
    else:
        value2 = None

    return {
            'obj': obj,
            'field': field_obj,
            'content_type_id': content_type_id,
            'form': form,
            'form_obj': form_obj,
            'value':  value,
            'value2':  value2,
            'empty_value': empty_value,
            'filters': simplejson.dumps(filters),
            'MEDIA_URL': context.get('MEDIA_URL',''),
            'user': context.get('user',None),
    }
register.inclusion_tag("inplace_edit.html", takes_context=True)(inplace_edit)

