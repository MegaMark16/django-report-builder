from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
from django.db import connection
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, EmptyPage

from models import Report
from forms import get_report_form

def GetPager(request, data):
    try:
        page_size = int(request.GET.get('page_size', '25'))
    except ValueError:
        page_size = 25

    paginator = Paginator(data, page_size) 
    try:
        page_number = int(request.GET.get('page_number', '1'))
    except ValueError:
        page_number = 1
    try:
        page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return page

@never_cache
@staff_member_required
def view_report(request, report_id):
    report = Report.objects.get(id=report_id)

    ReportForm = get_report_form(report)
    report_form = ReportForm()
    for item in request.GET:
        if item not in ('order_by','order_direction','page_number','page_size'):
            report_form = ReportForm(request.GET or None)
            break
    cursor = connection.cursor()
    params = {}
    parameters = report.reportparameter_set.all()
    for param in parameters:
        if report_form.is_valid():
            if report_form.cleaned_data.get(param.label):
                param.value = report_form.cleaned_data[param.label]
                params[param.label] = report_form.cleaned_data[param.label]
            else:
                params[param.label] = ''
        else:
            params[param.label] = param.default_value

    # Run main query
    try:
        cursor.execute(str(report.query), params)
    except Exception as ex:
        query = str(report.query % params)
        return render_to_response('report_builder/view_report.html', { 'query': query, 'ex': ex }, context_instance=RequestContext(request))

    headers = [c[0] for c in cursor.description]
    if request.GET.get('order_by') and request.GET['order_by'] in headers:
        if request.GET.get('order_direction') and request.GET['order_direction'] in ['ASC', 'DESC']:
            report.query += 'ORDER BY `%s` %s' % (request.GET['order_by'], request.GET['order_direction'])
        else:
            report.query += 'ORDER BY `%s`' % request.GET['order_by']
        try:
            cursor.execute(str(report.query), params)
        except Exception as ex:
            return render_to_response('report_builder/view_report.html', { 'query': str(report.query % params), 'ex': ex }, context_instance=RequestContext(request))

    results = cursor.fetchall()
    page = GetPager(request, results)
    results = page.object_list

    # If there is a Totals Query, try to run it
    totals_results = None
    totals_headers = None
    totals_ex = None
    if report.totals_query:
        try:
            cursor.execute(str(report.totals_query), params)
            totals_results = cursor.fetchall()
            totals_headers = [c[0] for c in cursor.description]
        except Exception as totals_ex: 
            totals_query = str(report.totals_query % params)
    
    response_perams = { 
        'results': results, 
        'page': page, 
        'headers': headers, 
        'parameters': parameters, 
        'query': str(report.query % params),
        'report_form': report_form,
        'totals_results': totals_results,
        'totals_headers': totals_headers,
        'totals_ex': totals_ex,
    }
    
    return render_to_response('report_builder/view_report.html', response_perams, context_instance=RequestContext(request))

