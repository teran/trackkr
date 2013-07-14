import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import timesince
from django.views.decorators.csrf import csrf_exempt


from core.models import Unit, Message


@login_required
def list(request):
    try:
        limit = int(request.GET['limit'])
    except:
        limit = 5

    try:
        cont_link = bool(request.GET['continue'])
    except:
        cont_link = True

    try:
        verbose = bool(request.GET['verbose'])
    except:
        verbose = False

    units = Unit.objects.filter(user=request.user)[:limit]
    return render_to_response('webui/units/units-list.html',
                              {'units': units, 'cont_link': cont_link, 'verbose': verbose},
                              context_instance=RequestContext(request))


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


def add_unit(request):
    try:
        imei = request.POST['imei']
        name = request.POST['name']
    except:
        return HttpResponseBadRequest(content=json.dumps({
            'status': 'error',
            'reason': 'Both of imei and name POST options are required'
        }), content_type='application/json')

    if request.user.is_authenticated:
        try:
            unit = Unit.objects.get(imei=imei, user=request.user)
            return HttpResponse(content=json.dumps({
                'status': 'error',
                'reasong': 'Unit witch such IMEI already exists'
            }), content_type='application/json')
        except:
            try:
                unit = Unit(name=name, imei=imei, user=request.user)
                unit.save()
                return HttpResponse(content=json.dumps({
                    'status': 'ok'
                }), content_type='application/json')
            except:
                return HttpResponseServerError(content=json.dumps({
                    'status': 'error',
                    'reason': 'Error occured while saving the unit'
                }), content_type='application/json')
    else:
        return HttpResponseForbidden(content=json.dumps({
            'status': 'error',
            'reason': 'not authenticated'
        }), content_type='application/json')


def delete_unit(request):
    try:
        imei = int(request.POST['imei'])
    except:
        return HttpResponseBadRequest(content=json.dumps({
            'status': 'error',
            'reason': 'imei POST option is required'
        }), content_type='application/json')

    if request.user.is_authenticated:
        try:
            unit = Unit.objects.get(imei=imei, user=request.user)
        except:
            return HttpResponseNotFound(content=json.dumps({
                'status': 'error',
                'reason': 'object not found'
            }), content_type='application/json')

        try:
            messages = Message.objects.filter(unit=unit).delete()
        except:
            pass

        unit.delete()

        return HttpResponse(content=json.dumps({
            'status': 'ok'
        }))
    else:
        return HttpResponseForbidden(content=json.dumps({
            'status': 'error',
            'reason': 'not authenticated'
        }), content_type='application/json')


@csrf_exempt
def checkin(request):
    try:
        imei = int(request.POST['imei'])
        mtype = str(request.POST['type'])
    except:
        return HttpResponseBadRequest(content=json.dumps({
            'status': 'error',
            'reason': 'all of imei, type, latitude and longitude POST options are required'
        }), content_type='application/json')

    try:
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
    except:
        latitude = None
        longitude = None

    if mtype not in ('logon', 'heartbeat', 'low_battery', 'sos', 'tracker'):
        return HttpResponseBadRequest(content=json.dumps({
            'status': 'error',
            'reason': 'allowed values for type: logon, heartbeat, low_battery, sos, tracker'
        }), content_type='application/json')

    try:
        u = Unit.objects.get(imei=imei)
    except:
        return HttpResponseNotFound(content=json.dumps({
            'status': 'error',
            'reason': 'unit not found'
        }))

    MESSAGE_TYPES = {
        'logon': 1,
        'heartbeat': 2,
        'low_battery': 3,
        'sos': 4,
        'tracker': 5
    }

    m = Message(
        message_type=MESSAGE_TYPES[mtype],
        latitude=latitude,
        longitude=longitude,
        unit=u
    )
    m.save()

    return HttpResponse(content=json.dumps({
        'status': 'ok'
    }), content_type='application/json')
