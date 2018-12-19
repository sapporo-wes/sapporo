# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserDetailTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        url = reverse("app:user_home", kwargs={"user_name": "TestUser"})
        response = client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        url = reverse("app:user_home", kwargs={"user_name": user.username})
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("user" in response.context)
        self.assertEqual(user, response.context['user'])
