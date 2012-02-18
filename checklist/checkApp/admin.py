from django.contrib import admin
from checkApp.models import CheckList, Task


class CheckListAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(CheckList, CheckListAdmin)


class CheckItemAdmin(admin.ModelAdmin):
    search_fields = ('text',)

admin.site.register(Task, CheckItemAdmin)
