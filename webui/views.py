from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from core.models import Unit


@login_required
def dashboard(request):
    units = Unit.objects.all()[:5]

    return render_to_response('webui/dashboard.html',
                              {'units': units},
                              context_instance=RequestContext(request))


def index(request):
    return redirect('/dashboard.html')


def log_in(request):
    if request.method == 'POST':
        try:
            nexturl = request.GET['next']
        except:
            nexturl = '/'

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(nexturl)
            else:
                # Return a 'disabled account' error message
                return render_to_response('webui/login.html',
                                          {'error': 'Account is disabled'},
                                          context_instance=RequestContext(request))
        else:
            # Return an 'invalid login' error message.
            return render_to_response('webui/login.html',
                                      {'error': 'Username or password is invalid'},
                                      context_instance=RequestContext(request))

    return render_to_response('webui/login.html',
                              {},
                              context_instance=RequestContext(request))


@login_required
def log_out(request):
    try:
        nexturl = request.GET['next']
    except:
        nexturl = '/'

    logout(request)

    return redirect(nexturl)


@login_required
def unit_add(request):
    if request.method == 'POST':
        try:
            nexturl = request.GET['next']
        except:
            nexturl = '/'
        try:
            name = request.POST['name']
            imei = request.POST['imei']

            if name == '' or imei == '':
                raise
        except:
            return render_to_response('webui/units/add.html',
                                      {'error': 'The both of name and IMEI fields are required'},
                                      context_instance=RequestContext(request))

        try:
            unit = Unit.objects.get_or_create(name=name, imei=imei)[0]
            unit.user.add(request.user)
            unit.save()
            return redirect(nexturl)
        except:
            return render_to_response('webui/units/add.html',
                                      {'error': 'Error saving the unit'},
                                      context_instance=RequestContext(request))

    return render_to_response('webui/units/add.html',
                              {},
                              context_instance=RequestContext(request))


@login_required
def unit_delete(request, imei):
    try:
        nexturl = request.GET['next']
    except:
        nexturl = '/'

    unit = get_object_or_404(Unit, imei=imei)

    unit.delete()

    return redirect(nexturl)


@login_required
def units(request):
    units = Unit.objects.all()
    return render_to_response('webui/units.html',
                              {'units': units},
                              context_instance=RequestContext(request))
