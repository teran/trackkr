import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, HttpResponse, Http404
from django.template import RequestContext

from core.models import Unit


@login_required
def lastpos(request, imei):
    unit = get_object_or_404(Unit, imei=imei)
    lastloc = unit.messages.filter(~Q(latitude=None, longitude=None)).order_by('-timestamp')[0]

    return HttpResponse(content=json.dumps({'latitude': lastloc.latitude,
                                            'longitude': lastloc.longitude,
                                            'timestamp': lastloc.timestamp.strftime('%Y-%m-%dT%H:%M:%S')}),
                        content_type='application/json')


@login_required
def units(request):
    units = Unit.objects.filter(user=request.user)

    return HttpResponse(content=json.dumps([{'imei':unit.imei, 'name':unit.name} for unit in units]),
                        content_type='application/json')
