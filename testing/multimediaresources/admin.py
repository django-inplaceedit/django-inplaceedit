from django.contrib import admin

from multimediaresources.models import TypeResource, Resource


class TypeResourceAdmin(admin.ModelAdmin):
    pass


class ResourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(TypeResource, TypeResourceAdmin)
admin.site.register(Resource, ResourceAdmin)
