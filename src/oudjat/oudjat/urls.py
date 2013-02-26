from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oudjat.views.home', name='home'),
    # url(r'^oudjat/', include('oudjat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

      url(r'^search/$', 'search.views.index'),
     # url(r'^search/(?P<search_id>\d+)', 'search.views.detail'),                    
      url(r'^search/view/$', 'search.views.view'),
      url(r'^search/add/$', 'search.views.add'),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)
