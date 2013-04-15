import csv
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model
from apps.friends.views import json_view
from apps.stunable_search.models import Flavor
from tagging.models import Tag
from apps.racks.models import Item
from apps.retailers.models import RetailerProfile

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = [field.name for field in model._meta.fields]
    
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                if type(val) == unicode:
                    val = val.encode('utf-8')
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def export_average(qs, fields):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)

    writer.writerow(['brand', 'average_price'])
    
    acum = {} # 'brand': {, sum: , count: })
    
    for obj in qs:
        brand = obj.brand.strip()
        if brand not in acum:
            acum[brand] = {'sum': 0, 'count': 0 }
        price = float(obj.price)

        acum[brand]['sum'] += price
        acum[brand]['count'] += 1
    
    rows = []
    
    for (brand, value) in acum.items():
        av = value['sum']/value['count']
        av = float("%.02f" % av)
        r = [str(brand), av]
        rows.append(r)
        
    rows.sort()
    
    for r in rows:
        writer.writerow(r)
    
    return response

def admin_list_export(request, model_name, app_label, queryset=None, fields=None, list_display=True):
    """
    Put the following line in your urls.py BEFORE your admin include
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'common.views.admin_list_export'),
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if not queryset:
        model = get_model(app_label, model_name)
        queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            if key not in ('ot', 'o'):
                filters[str(key)] = str(value)
        if len(filters):
            queryset = queryset.filter(**filters)
    if not fields:
        try:
            if list_display and len(queryset.model._meta.admin.list_display) > 1:
                fields = queryset.model._meta.admin.list_display
            else:
                fields = None
        except:
            fields = None
    if request.GET.get('o') == 'cal_average':
        return export_average(queryset, fields)
    
    return export(queryset, fields)


def lookup(request, model_name, app_label, queryset=None, fields=None, list_display=True):
    model = get_model(app_label, model_name)
    qs = model.objects.all()
    if request.GET.get('term',None):
        out = qs.filter(name__istartswith=request.GET.get('term'))
    return HttpResponse(json.dumps([{'slug':o.slug,'label':o.name,'value':o.slug} for o in out]),mimetype="application/json")


def combo_lookup(request):
    if request.GET.get('term',None):
        flavors = Flavor.objects.filter(name__icontains=request.GET.get('term')).order_by('group')
        # tags = Tag.objects.filter(name__istartswith=request.GET.get('term'))
        items = Item.objects.carousel_items().filter(name__icontains=request.GET.get('term')).order_by('name')[:20]
        retailers = RetailerProfile.objects.filter(name__icontains=request.GET.get('term'))

    return HttpResponse(json.dumps(
            [{'category':'stylist','slug':o.slug,'label':o.name,'value':o.slug} for o in retailers]+
            [{'category':o.group,'slug':o.slug,'label':o.name,'value':o.slug} for o in flavors]+
            # [{'category':'keyword','slug':o.slug,'label':o.name,'value':o.slug} for o in tags]+
            [{'category':'product','slug':o.slug,'label':o.name,'value':o.slug} for o in items]
        # }
        ),mimetype="application/json")


