from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext


@login_required
def dashboard(request):
    return render_to_response('webui/dashboard.html',
                              {},
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
                pass
        else:
            # Return an 'invalid login' error message.
            pass

    return render_to_response('webui/login.html',
                              {},
                              context_instance=RequestContext(request))


def log_out(request):
    try:
        nexturl = request.GET['next']
    except:
        nexturl = '/'

    logout(request)

    return redirect(nexturl)


@login_required
def units(request):
    return render_to_response('webui/units.html',
                              {},
                              context_instance=RequestContext(request))
