# -*- coding: utf-8 -*-
from django import template
from django.forms.models import modelform_factory, ModelMultipleChoiceField
from django.forms.fields import MultipleChoiceField
from django.contrib.contenttypes.models import ContentType

def change_foreing_key(obj):
    obj_dict = obj.__dict__
    obj_dict_result = obj_dict.copy()
    for key, value in obj_dict.items():
        if '_id' in key:
            key2 = key.replace('_id','')
            obj_dict_result[key2] = obj_dict_result[key]
            del obj_dict_result[key]

    manytomany_list = obj._meta.many_to_many
    for manytomany in manytomany_list:
        obj_dict_result[manytomany.name] = [ obj_rel.id for obj_rel in manytomany.value_from_object(obj)]
    return obj_dict_result


def apply_filters(value, filters):
    if filters:
        filters_str = '|%s' % '|'.join(filters)
        value = template.Template("""{{ value%s }}""" % filters_str).render(template.Context({'value': value}))
    return value


def get_form_class(form_str=None, content_type_id=None):
    if form_str:
        path_split = form_str.split('.')
        return getattr(__import__('.'.join(path_split[:len(path_split)-1]), {}, {}, [path_split[len(path_split)-1]]), path_split[(len(path_split)-1)])
    contenttype = ContentType.objects.get(id=content_type_id)
    return modelform_factory(contenttype.model_class())


def special_procesing(field_obj, value):
    if isinstance(field_obj.field, MultipleChoiceField) or isinstance(field_obj.field, ModelMultipleChoiceField):
        value = value.all()
        value =[v.__unicode__() for v in value]
        value = ','.join(value)

    if field_obj.form._meta.model._meta.get_field(field_obj.name) and field_obj.form._meta.model._meta.get_field(field_obj.name).choices:
        choices_dict = dict(field_obj.form._meta.model._meta.get_field(field_obj.name).choices)
        value = choices_dict[value]

    return value
