from django.conf.urls.defaults import *

urlpatterns = patterns('report_builder.views',
    url(r'^(?P<report_id>\d+)/$', 'view_report', name='view_report'),
)
