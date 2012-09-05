# -*- coding: utf-8 -*-
from django import template
from django.template import Library, Variable
from django.conf import settings
from django.utils import simplejson

from inplaceeditform.commons import get_adaptor_class, get_static_url, get_admin_static_url
from inplaceeditform.tag_utils import RenderWithArgsAndKwargsNode, parse_args_kwargs

register = Library()


def inplace_js(context, activate_inplaceedit=True, toolbar=False):
    return context.update({
        'STATIC_URL': get_static_url(),
        'ADMIN_MEDIA_PREFIX': get_admin_static_url(),
        'activate_inplaceedit': activate_inplaceedit,
        'auto_save': simplejson.dumps(getattr(settings, "INPLACEEDIT_AUTO_SAVE", False)),
        'event': getattr(settings, "INPLACEEDIT_EVENT", "dblclick"),
        'disable_click': simplejson.dumps(getattr(settings, "INPLACEEDIT_DISABLE_CLICK", True)),
        'toolbar': toolbar,
    })
register.inclusion_tag("inplaceeditform/inplace_js.html", takes_context=True)(inplace_js)


def inplace_css(context, toolbar=False):
    return context.update({
        'STATIC_URL': get_static_url(),
        'ADMIN_MEDIA_PREFIX': get_admin_static_url(),
        'toolbar': toolbar,
    })
register.inclusion_tag("inplaceeditform/inplace_css.html", takes_context=True)(inplace_css)


def inplace_static(context):
    return context.update({
        'STATIC_URL': get_static_url(),
        'ADMIN_MEDIA_PREFIX': get_admin_static_url(),
        'toolbar': False,
    })
register.inclusion_tag("inplaceeditform/inplace_static.html", takes_context=True)(inplace_static)


#to old django versions
def inplace_media(context):
    return inplace_static(context)
register.inclusion_tag("inplaceeditform/inplace_static.html", takes_context=True)(inplace_media)


def inplace_toolbar(context):
    return context.update({
        'STATIC_URL': get_static_url(),
        'ADMIN_MEDIA_PREFIX': get_admin_static_url(),
        'toolbar': True,
    })
register.inclusion_tag("inplaceeditform/inplace_static.html", takes_context=True)(inplace_toolbar)


class InplaceEditNode(RenderWithArgsAndKwargsNode):

    def prepare_context(self, args, kwargs, context):
        expression_to_show = args[0]
        tokens_to_show = expression_to_show.split('|')
        obj_field_name, filters_to_show = tokens_to_show[0], '|'.join(tokens_to_show[1:])
        obj_field_name_split = obj_field_name.split(".")
        obj_context = '.'.join(obj_field_name_split[:-1])
        field_name = obj_field_name_split[-1]
        obj = Variable(obj_context).resolve(context)
        adaptor = kwargs.get('adaptor', None)
        class_adaptor = get_adaptor_class(adaptor, obj, field_name)
        request = context.get('request')

        config = class_adaptor.get_config(**kwargs)

        adaptor_field = class_adaptor(request, obj, field_name,
                                               filters_to_show,
                                               config)

        context = {
            'adaptor_field': adaptor_field,
        }
        return context


@register.tag
def inplace_edit(parser, token):
    args, kwargs = parse_args_kwargs(parser, token)
    return InplaceEditNode(args, kwargs, 'inplaceeditform/inplace_edit.html')


@register.tag(name='eval')
def do_eval(parser, token):
    "Usage: {% eval %}1 + 1{% endeval %}"

    nodelist = parser.parse(('endeval',))

    class EvalNode(template.Node):
        def render(self, context):
            return template.Template(nodelist.render(context)).render(template.Context(context))
    parser.delete_first_token()
    return EvalNode()
