from django.contrib import messages
from django.shortcuts import redirect, render

from services.models import Service

from .forms import ContactForm
from .models import Doctor, SiteSettings


def home(request):
    settings_obj = SiteSettings.load()
    services = Service.objects.filter(is_active=True)[:6]
    doctors = Doctor.objects.filter(is_active=True)[:3]

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Ваша заявка отправлена, мы свяжемся с вами.")
            return redirect("core:home")
    else:
        form = ContactForm()

    context = {
        "settings": settings_obj,
        "services": services,
        "doctors": doctors,
        "form": form,
    }
    return render(request, "core/home.html", context)


def about(request):
    settings_obj = SiteSettings.load()
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, "core/about.html", {"settings": settings_obj, "doctors": doctors})


def contacts(request):
    settings_obj = SiteSettings.load()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Ваша заявка отправлена, мы свяжемся с вами.")
            return redirect("core:contacts")
    else:
        form = ContactForm()

    return render(request, "core/contacts.html", {"settings": settings_obj, "form": form})