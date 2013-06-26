from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from models import Report, ReportParameter
from views import view_report

class ReportParameterInline(admin.StackedInline):
    model = ReportParameter
    extra = 1

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    class Meta:
        model = Report
    inlines = [
        ReportParameterInline,
    ]

    def get_urls(self):
        old_urls = super(ReportAdmin, self).get_urls()
        new_urls = patterns('',
            url(r'^(?P<report_id>\d+)/view/$', view_report, name='admin_view_report'),
        )
        return new_urls + old_urls

admin.site.register(Report, ReportAdmin)

