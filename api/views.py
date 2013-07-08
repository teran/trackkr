import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import timesince

from core.models import Unit, Message


@login_required
def location(request):
    try:
        imei = int(request.GET['imei'])
    except:
        units = Unit.objects.filter(user=request.user)
        out = []
        for unit in units:
            location = unit.get_lastlocation()

            if location is not None:
                out.append({
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'name': location.unit.name,
                    'timestamp': str(location.timestamp)
                })

        return HttpResponse(content=json.dumps(out),
                            content_type='application/json')

    if request.GET.has_key('message'):
        messageid = int(request.GET['message'])
        message = get_object_or_404(Message, pk=messageid, unit__imei=imei, unit__user=request.user)

        return HttpResponse(content=json.dumps({
            'longitude': message.longitude,
            'latitude': message.latitude,
            'name': message.unit.name,
            'timestamp': str(message.timestamp)
        }), content_type='application/json')
    else:
        unit = get_object_or_404(Unit, imei=imei, user=request.user)
        location = unit.get_lastlocation()

        try:
            return HttpResponse(content=json.dumps({
                'longitude': location.longitude,
                'latitude': location.latitude,
                'name': location.unit.name,
                'timestamp': str(location.timestamp)
            }), content_type='application/json')
        except:
            return HttpResponse(content=json.dumps({
                'longitude': None,
                'latitude': None,
                'name': unit.name,
                'timestamp': None
            }), content_type='application/json')
