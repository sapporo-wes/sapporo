# coding: utf-8
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase

from app.forms import ServiceAdditionForm, UserCreationForm


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

    def test_create_user_commit_true(self):
        params = {
            "username": "TestUser",
            "email": "test@test.com",
            "password1": "TestPass012",
            "password2": "TestPass012",
        }
        form = UserCreationForm(params)
        if form.is_valid():
            user = form.save()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, params["username"])
            self.assertEqual(user.email, params["email"])

    def test_create_user_commit_false(self):
        params = {
            "username": "TestUser",
            "email": "test@test.com",
            "password1": "TestPass012",
            "password2": "TestPass012",
        }
        form = UserCreationForm(params)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = "test2@test.com"
            user.save()
            user = User.objects.get(username=params["username"])
            self.assertNotEqual(params["email"], user.email)


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
