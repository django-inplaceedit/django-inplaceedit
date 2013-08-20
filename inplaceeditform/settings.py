from django.conf import settings
from django.utils.translation import ugettext_lazy as _


INPLACEEDIT_EDIT_EMPTY_VALUE = (getattr(settings, 'INPLACEEDIT_EDIT_EMPTY_VALUE', None) and
                                _(settings.INPLACEEDIT_EDIT_EMPTY_VALUE) or _('Doubleclick to edit'))
INPLACEEDIT_AUTO_SAVE = getattr(settings, 'INPLACEEDIT_AUTO_SAVE', False)
INPLACEEDIT_EVENT = getattr(settings, 'INPLACEEDIT_EVENT', 'dblclick')
INPLACEEDIT_DISABLE_CLICK = getattr(settings, 'INPLACEEDIT_DISABLE_CLICK', True)
INPLACEEDIT_EDIT_MESSAGE_TRANSLATION = (getattr(settings, 'INPLACEEDIT_EDIT_MESSAGE_TRANSLATION', None) and
                                        _(settings.INPLACEEDIT_EDIT_MESSAGE_TRANSLATION) or _('Write a translation'))
DEFAULT_INPLACE_EDIT_OPTIONS = getattr(settings, "DEFAULT_INPLACE_EDIT_OPTIONS", {})
DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE = getattr(settings, 'DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE', False)

ADAPTOR_INPLACEEDIT_EDIT = getattr(settings, 'ADAPTOR_INPLACEEDIT_EDIT', None)
ADAPTOR_INPLACEEDIT = getattr(settings, 'ADAPTOR_INPLACEEDIT', {})
