from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('search.views',
                       url(r'^search/$', 'index'),
                       url(r'^search/view/$', 'view'),
                       url(r'^search/add/$', 'add'),
                       url(r'^search/results/$', 'results'),
                       url(r'^search/results/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$','report_details', name='report_details'),
                       url(r'^search/results/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pageid>\d{1,2})/$', 'ticket', name='ticket'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
