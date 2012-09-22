from django.contrib import admin

from test_fk.models import *

admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Document)
