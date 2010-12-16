from django.conf.urls.defaults import *

urlpatterns = patterns('report_builder.views',
    (r'^(?P<report_id>\d+)/$', 'view_report'),
)
