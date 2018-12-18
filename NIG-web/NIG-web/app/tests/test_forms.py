from django.test import TestCase
from app.forms import UserCreationForm
from app.forms import ServiceAdditionForm


class UserCreationFormTests(TestCase):
    def test_valid(self):
        params = {
            "username": "TestUser",
            "email": "test@test.com",
            "password1": "TestPass012",
            "password2": "TestPass012",
        }
        form = UserCreationForm(params)
        self.assertTrue(form.is_valid())
        for key, value in params.items():
            self.assertTrue(form.cleaned_data[key], value)

    def test_easy_password(self):
        params = {
            "username": "TestUser",
            "email": "test@test.com",
            "password1": "password",
            "password2": "password",
        }
        form = UserCreationForm(params)
        self.assertFalse(form.is_valid())

    def test_wrong_password(self):
        params = {
            "username": "TestUser",
            "email": "test@test.com",
            "password1": "TestPass012",
            "password2": "TestPass000",
        }
        form = UserCreationForm(params)
        self.assertFalse(form.is_valid())


class ServiceAdditionFormTests(TestCase):
    def test_valid(self):
        params = {
            "service_name": "TestService",
            "api_server_url": "localhost:9999",
        }
        form = ServiceAdditionForm(params)
        self.assertTrue(form.is_valid())
        for key, value in params.items():
            self.assertTrue(form.cleaned_data[key], value)

    def test_wrong_api_server_url(self):
        params = {
            "service_name": "TestService",
            "api_server_url": "localhost:9998",
        }
        form = ServiceAdditionForm(params)
        self.assertFalse(form.is_valid())
        for key, value in params.items():
            self.assertTrue(form.cleaned_data[key], value)
