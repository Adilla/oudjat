from search.models import Word
from search.models import Domain
from search.models import Option
from search.models import Research
from django.contrib import admin

class OptionAdmin(admin.ModelAdmin):
     list_display = ('name', 'description')


admin.site.register(Word)
admin.site.register(Domain)
admin.site.register(Option, OptionAdmin)
admin.site.register(Research)
