from django.contrib import admin
from models import Report, ReportParameter

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
    
admin.site.register(Report, ReportAdmin)

