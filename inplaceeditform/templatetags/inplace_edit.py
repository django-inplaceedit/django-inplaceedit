# -*- coding: utf-8 -*-
from django import template
from django.template import Library, Variable
from django.conf import settings

from inplaceeditform.commons import get_adaptor_class
from inplaceeditform.tag_utils import RenderWithArgsAndKwargsNode, parse_args_kwargs

register = Library()


def inplace_js(context, activate_inplaceedit=True):
    return context.update({
            'MEDIA_URL': context.get('MEDIA_URL', settings.MEDIA_URL),
            'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
            'activate_inplaceedit': activate_inplaceedit,
    })
register.inclusion_tag("inplaceeditform/inplace_js.html", takes_context=True)(inplace_js)


def inplace_css(context):
    return context.update({
            'MEDIA_URL': context.get('MEDIA_URL', settings.MEDIA_URL),
            'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
    })
register.inclusion_tag("inplaceeditform/inplace_css.html", takes_context=True)(inplace_css)


def inplace_media(context):
    return context.update({
            'MEDIA_URL': context.get('MEDIA_URL', settings.MEDIA_URL),
            'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
    })
register.inclusion_tag("inplaceeditform/inplace_media.html", takes_context=True)(inplace_media)


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
