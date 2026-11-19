import pytest
from django.contrib.auth import get_user_model

from core.models import SiteSettings
from services.models import Service


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="patient", password="testpass123")


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )


@pytest.fixture
def site_settings(db):
    return SiteSettings.load()


@pytest.fixture
def service(db):
    return Service.objects.create(
        name="Общий анализ крови",
        slug="obshhij-analiz-krovi",
        short_description="Базовое исследование",
        price=800,
    )
