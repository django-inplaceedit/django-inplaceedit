from django.contrib import admin

from testing.unusual_fields.models import UnusualModel


class UnusualModelAdmin(admin.ModelAdmin):
    pass


class ResourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(UnusualModel, UnusualModelAdmin)
