import pytest
from django.urls import reverse

from core.forms import ContactForm
from core.models import ContactRequest, Doctor, SiteSettings


@pytest.mark.django_db
class TestSiteSettings:
    def test_singleton(self):
        s1 = SiteSettings.load()
        s2 = SiteSettings.load()
        assert s1.pk == s2.pk == 1

    def test_str(self, site_settings):
        site_settings.company_name = "МедЦентр"
        site_settings.save()
        assert str(site_settings) == "МедЦентр"


@pytest.mark.django_db
class TestContactRequest:
    def test_create(self):
        req = ContactRequest.objects.create(name="Иван", message="Привет")
        assert req.is_processed is False
        assert "Иван" in str(req)


@pytest.mark.django_db
class TestDoctor:
    def test_str(self):
        doc = Doctor.objects.create(full_name="Иванов Иван", specialization="Терапевт")
        assert "Иванов Иван" in str(doc)


@pytest.mark.django_db
class TestContactForm:
    def test_valid(self):
        form = ContactForm(data={"name": "Иван", "message": "Текст", "phone": "", "email": ""})
        assert form.is_valid()

    def test_invalid_no_name(self):
        form = ContactForm(data={"message": "Текст"})
        assert not form.is_valid()
        assert "name" in form.errors


@pytest.mark.django_db
class TestViews:
    def test_home_200(self, client, site_settings):
        response = client.get(reverse("core:home"))
        assert response.status_code == 200

    def test_about_200(self, client, site_settings):
        response = client.get(reverse("core:about"))
        assert response.status_code == 200

    def test_contacts_200(self, client, site_settings):
        response = client.get(reverse("core:contacts"))
        assert response.status_code == 200

    def test_contact_form_post(self, client, site_settings):
        response = client.post(
            reverse("core:contacts"),
            {"name": "Пётр", "message": "Здравствуйте", "phone": "", "email": ""},
        )
        assert response.status_code == 302
        assert ContactRequest.objects.filter(name="Пётр").exists()