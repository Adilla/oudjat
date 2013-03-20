from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()


#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oudjat.views.home', name='home'),
    # url(r'^oudjat/', include('oudjat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

 #     url(r'^search/$', 'search.views.index'),
     # url(r'^search/(?P<search_id>\d+)', 'search.views.detail'),                    
 #     url(r'^search/view/$', 'search.views.view'),
 #     url(r'^search/add/$', 'search.views.add'),

    # Uncomment the next line to enable the admin:
 #     url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns = patterns('search.views',
                       url(r'^search/$', 'index'),
                       url(r'^search/view/$', 'view'),
                       url(r'^search/add/$', 'add'),
                       url(r'^search/results/$', 'results'),
                       url(r'^search/results/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'details', name='details_test'),
                       url(r'^admin/', include(admin.site.urls)),

)
