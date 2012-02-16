from django.contrib import admin
from checkApp.models import CheckList


class CheckListAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(CheckList,CheckListAdmin)