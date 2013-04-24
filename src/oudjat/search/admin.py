"""
Admin interface management
"""

from search.models import *
from django.contrib import admin

class OptionAdmin(admin.ModelAdmin):
     """ Admin interface for module Option """
     list_display = ('name', 'description')

class CrontabAdmin(admin.ModelAdmin):
     """ Admin interface for Crontab """
     list_display = ('id', 
                     'priority', 
                     'number_of_researches', 
                     'has_reached_limit')

class ResearchAdmin(admin.ModelAdmin):
     """ Admin interface for Research """
     list_display = ('words', 'cron', 'is_done')

admin.site.register(Word)
admin.site.register(Domain)
admin.site.register(Option, OptionAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Crontab, CrontabAdmin)
