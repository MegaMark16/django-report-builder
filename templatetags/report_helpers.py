from django import template

register = template.Library()

SORT_DIRECTIONS = {'ASC': 'DESC', 'DESC': 'ASC',}

@register.filter
def sort_link(link, request):
    querystring_list = ['order_by=%s' % link,]
    if request.GET.get('order_by') == link:
        if request.GET.get('order_direction'):
            querystring_list.append('order_direction=%s' % SORT_DIRECTIONS[request.GET['order_direction']])
        else:
            querystring_list.append('order_direction=DESC')
    for item in request.GET:
        if item not in ['order_by', 'order_direction']:
            querystring_list.append('%s=%s' % (item, request.GET[item]))
    return '&'.join(querystring_list)

