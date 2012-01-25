

class SuperUserPermEditInline(object):

    @classmethod
    def can_edit(cls, field):
        return field.request.user.is_authenticated and field.request.user.is_superuser


class AdminDjangoPermEditInline(SuperUserPermEditInline):

    @classmethod
    def can_edit(cls, field):
        is_super_user = super(AdminDjangoPermEditInline, cls).can_edit(field)
        if not is_super_user:
            model = field.model
            model_edit = '%s.change_%s' % (model._meta.app_label,
                                           model._meta.module_name)
            return field.request.user.has_perm(model_edit)
        return is_super_user
