
from django.contrib import admin

from mongo_storage.admin import MongoFileAdminMixin, DeleteActionMixin
from sample import models

class SampleAdmin(MongoFileAdminMixin, admin.ModelAdmin):
    list_display = ['display_name', 'file_name', 'file_size']

class SampleDeleteAdmin(DeleteActionMixin, MongoFileAdminMixin, admin.ModelAdmin):
    list_display = ['display_name', 'file_name', 'file_size']
    actions = ['delete_selected']

admin.site.register(models.SampleModel, SampleAdmin)
admin.site.register(models.SampleDeleteModel, SampleDeleteAdmin)