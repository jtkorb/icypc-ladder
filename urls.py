from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^ladder/challenge/', 'ladder.views.challenge'),
    (r'^ladder/rebuild/', 'ladder.views.rebuild'),
    (r'^ladder/', 'ladder.views.index'),
)
