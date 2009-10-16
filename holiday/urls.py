from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^holiday/$', 'holiday.main.views.index'),
    (r'^holiday/html/$', 'holiday.main.views.html_index'),
    (r'^holiday/html/(\d{4})/$', 'holiday.main.views.html'),
    (r'^holiday/ics/$', 'holiday.main.views.ics'),
    (r'^holiday/xml/$', 'holiday.main.views.xml'),
    (r'^admin/(.*)', admin.site.root),
)
