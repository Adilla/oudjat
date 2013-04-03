from search.models import *

from django.contrib import admin

class OptionAdmin(admin.ModelAdmin):
     list_display = ('name', 'description')


admin.site.register(Word)
admin.site.register(Domain)
admin.site.register(Option, OptionAdmin)
admin.site.register(Research)
admin.site.register(Crontab)
