import datetime

import pytest
from django.urls import reverse

from appointments.forms import AppointmentForm
from appointments.models import Appointment, DiagnosticResult


@pytest.mark.django_db
class TestAppointmentModel:
    def test_create(self, user, service):
        a = Appointment.objects.create(
            user=user,
            service=service,
            date=datetime.date(2026, 12, 1),
            time=datetime.time(10, 0),
        )
        assert a.status == Appointment.STATUS_NEW
        assert str(a).startswith("patient")


@pytest.mark.django_db
class TestDiagnosticResult:
    def test_create(self, user, service):
        a = Appointment.objects.create(
            user=user, service=service, date=datetime.date(2026, 12, 1), time=datetime.time(10, 0)
        )
        r = DiagnosticResult.objects.create(appointment=a, conclusion="Всё хорошо")
        assert "Всё хорошо" in r.conclusion


@pytest.mark.django_db
class TestAppointmentForm:
    def test_valid(self, service):
        form = AppointmentForm(
            data={
                "service": service.pk,
                "date": "2026-12-01",
                "time": "10:00",
                "comment": "",
            }
        )
        assert form.is_valid()


@pytest.mark.django_db
class TestAppointmentViews:
    def test_list_requires_login(self, client):
        response = client.get(reverse("appointments:list"))
        assert response.status_code == 302

    def test_list_ok(self, client, user):
        client.force_login(user)
        response = client.get(reverse("appointments:list"))
        assert response.status_code == 200

    def test_create_ok(self, client, user, service, site_settings):
        client.force_login(user)
        response = client.post(
            reverse("appointments:create"),
            {"service": service.pk, "date": "2026-12-01", "time": "10:00", "comment": ""},
        )
        assert response.status_code == 302
        assert Appointment.objects.filter(user=user).exists()

    def test_detail_other_user_404(self, client, admin_user, user, service):
        a = Appointment.objects.create(
            user=admin_user, service=service, date=datetime.date(2026, 12, 1), time=datetime.time(10, 0)
        )
        client.force_login(user)
        response = client.get(reverse("appointments:detail", kwargs={"pk": a.pk}))
        assert response.status_code == 404
