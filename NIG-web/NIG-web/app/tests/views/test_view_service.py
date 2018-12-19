# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import Service


class ServiceListViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:service_list"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:service_list"))
        self.assertEquals(response.status_code, 200)

    def test_post_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.post(reverse("app:service_list"))
        self.assertEquals(response.status_code, 302)

    def test_post_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.post(reverse("app:service_list"))
        self.assertEquals(response.status_code, 200)

    def test_post_service_addition_form(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        params = {
            "service_name": "TestService",
            "api_server_url": "localhost:9999",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:service_list"), params)
        self.assertEquals(response.status_code, 200)
        service = Service.objects.get(name=params["service_name"])
        self.assertIsNotNone(service)

    def test_post_service_addition_form_error(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        params = {
            "service_name": "TestService",
            "api_server_url": "localhost:9998",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:service_list"), params)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Please enter the correct URL.")


class ServiceDetailViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:service_detail"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:service_detail", kwargs={
            "service_name": "service_name"}))
        self.assertEquals(response.status_code, 200)
