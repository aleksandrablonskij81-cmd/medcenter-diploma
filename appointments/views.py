from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm
from .models import Appointment


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user).select_related("service")
    return render(request, "appointments/list.html", {"appointments": appointments})


@login_required
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect("appointments:list")
    else:
        form = AppointmentForm()
    return render(request, "appointments/form.html", {"form": form})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    return render(request, "appointments/detail.html", {"appointment": appointment})