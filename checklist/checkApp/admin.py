from django.contrib import admin
from checkApp.models import CheckList, Task, Template


class CheckListAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(CheckList, CheckListAdmin)


class CheckItemAdmin(admin.ModelAdmin):
    search_fields = ('text',)

admin.site.register(Task, CheckItemAdmin)


class TemplateAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Template, TemplateAdmin)
