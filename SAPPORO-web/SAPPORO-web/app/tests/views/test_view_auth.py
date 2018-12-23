# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class SigninViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:signin"))
        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:signin"))
        self.assertEquals(response.status_code, 200)


class SignoutViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:signout"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:signout"))
        self.assertEquals(response.status_code, 302)


class SignupViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:signup"))
        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:signup"))
        self.assertEquals(response.status_code, 200)
