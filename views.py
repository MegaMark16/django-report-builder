from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
from django.db import connection

from models import Report
from forms import get_report_form
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def view_report(request, report_id):
    report = Report.objects.get(id=report_id)
    
    ReportForm = get_report_form(report)
    report_form = ReportForm(request.GET or None)
    
    cursor = connection.cursor()
    params = {}
    parameters = report.reportparameter_set.all()
    for param in parameters:
        if report_form.is_valid() and report_form.cleaned_data.get(param.label):
            param.value = report_form.cleaned_data[param.label]
            params[param.label] = report_form.cleaned_data[param.label]
        else:
            params[param.label] = param.default_value
    
    try:
        cursor.execute(str(report.query), params)
    except Exception as ex: 
        query = str(report.query % params)
        return render_to_response('report_builder/view_report.html', { 'query': query, 'ex': ex }, context_instance=RequestContext(request))
        
    headers = [c[0] for c in cursor.description]
    if request.GET.get('order_by'):
        if request.GET['order_by'] in headers:
            if request.GET.get('order_direction') and request.GET['order_direction'] in ['ASC', 'DESC']:
                report.query += 'ORDER BY `%s` %s' % (request.GET['order_by'], request.GET['order_direction'])
            else:
                report.query += 'ORDER BY `%s`' % request.GET['order_by']
            try:
                cursor.execute(str(report.query), params)
            except Exception as ex:
                return render_to_response('report_builder/view_report.html', { 'query': str(report.query % params), 'ex': ex }, context_instance=RequestContext(request))
        
    results = cursor.fetchall()
    
    response_perams = { 
        'results': results, 
        'headers': headers, 
        'parameters': parameters, 
        'query': str(report.query % params),
        'report_form': report_form,
    }
    
    return render_to_response('report_builder/view_report.html', response_perams, context_instance=RequestContext(request))

