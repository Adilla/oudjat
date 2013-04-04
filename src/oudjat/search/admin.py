from search.models import *

from django.contrib import admin

class OptionAdmin(admin.ModelAdmin):
     list_display = ('name', 'description')

class CrontabAdmin(admin.ModelAdmin):
     list_display = ('priority', 'number_of_researches', 'has_reached_limit')

admin.site.register(Word)
admin.site.register(Domain)
admin.site.register(Option, OptionAdmin)
admin.site.register(Research)
admin.site.register(Crontab, CrontabAdmin)
