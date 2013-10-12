import datetime
from django.shortcuts import redirect, render_to_response, render
from windberg_register.forms import AppointmentForm
from windberg_register.models import Version


def register(request):
    version = Version.current_active()
    if version is None:
        return render(request, "register/registration_end.html", {})
    if datetime.datetime.combine(version.net_end, datetime.time()) <= datetime.datetime.now():
        return render(request, "register/registration_end.html", {})

    if request.method == 'POST': # If the form has been submitted...
        form = AppointmentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return redirect("windberg_register_success")
    else:
        form = AppointmentForm() # An unbound form

    return render(request, "register/registration_form.html",  {'form': form})


def allowed_starts(request):
    pass


