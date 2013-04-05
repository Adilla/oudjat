from report.models import Page
from report.models import Result
from django.contrib import admin

class ResultAdmin(admin.ModelAdmin):
    list_display = ('word', 'page', 'occurences', 'date')

class PageAdmin(admin.ModelAdmin):
    list_display = ('sitename', 'path', 'ticket')

admin.site.register(Result, ResultAdmin)
admin.site.register(Page, PageAdmin)
