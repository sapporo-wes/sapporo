# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class DataListViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:data_list"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:data_list"))
        self.assertEquals(response.status_code, 200)


class DataDetailViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:data_detail"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:data_detail", kwargs={
            "data_unique_id": "data_unique_id"}))
        self.assertEquals(response.status_code, 200)
