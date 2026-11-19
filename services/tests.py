import pytest
from django.urls import reverse

from services.models import Service


@pytest.mark.django_db
class TestServiceModel:
    def test_str(self, service):
        assert str(service) == "Общий анализ крови"

    def test_get_absolute_url(self, service):
        url = service.get_absolute_url()
        assert url == reverse("services:detail", kwargs={"slug": service.slug})


@pytest.mark.django_db
class TestServiceViews:
    def test_list_200(self, client, site_settings, service):
        response = client.get(reverse("services:list"))
        assert response.status_code == 200
        assert "Общий анализ крови" in response.content.decode()

    def test_detail_200(self, client, site_settings, service):
        response = client.get(service.get_absolute_url())
        assert response.status_code == 200

    def test_detail_404(self, client, site_settings):
        response = client.get(reverse("services:detail", kwargs={"slug": "nope"}))
        assert response.status_code == 404