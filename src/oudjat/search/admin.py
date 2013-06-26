"""
Admin interface management
"""

from search.models import Word, Domain, Option, Search, Crontab
from django.contrib import admin

class OptionAdmin(admin.ModelAdmin):
    """ Admin interface for module Option """
    list_display = ('name', 'description')

class CrontabAdmin(admin.ModelAdmin):
    """ Admin interface for Crontab """
    list_display = ('id', 
                    'priority', 
                    'number_of_searches', 
                    'has_reached_limit')

class SearchAdmin(admin.ModelAdmin):
    """ Admin interface for Search """
    list_display = ('words', 'cron', 'is_done')

admin.site.register(Word)
admin.site.register(Domain)
admin.site.register(Option, OptionAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Crontab, CrontabAdmin)
