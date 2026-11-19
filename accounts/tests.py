import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.forms import RegisterForm


@pytest.mark.django_db
class TestUserModel:
    def test_str(self):
        User = get_user_model()
        u = User.objects.create_user(username="test", password="pass12345")
        assert str(u) == "test"


@pytest.mark.django_db
class TestRegisterForm:
    def test_valid(self):
        form = RegisterForm(
            data={
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        assert form.is_valid()

    def test_passwords_mismatch(self):
        form = RegisterForm(
            data={
                "username": "newuser",
                "password1": "StrongPass123!",
                "password2": "OtherPass123!",
            }
        )
        assert not form.is_valid()


@pytest.mark.django_db
class TestAuthViews:
    def test_register_page(self, client):
        response = client.get(reverse("accounts:register"))
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get(reverse("accounts:login"))
        assert response.status_code == 200

    def test_profile_requires_login(self, client):
        response = client.get(reverse("accounts:profile"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_profile_ok(self, client, user):
        client.force_login(user)
        response = client.get(reverse("accounts:profile"))
        assert response.status_code == 200
