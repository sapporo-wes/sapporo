# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import Service, Workflow


class AdminHomeViewTests(TestCase):
    def test_get_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:admin_home"))
        self.assertEquals(response.status_code, 403)

    def test_get_not_super_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:admin_home"))
        self.assertEquals(response.status_code, 403)

    def test_get_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:admin_home"))
        self.assertEquals(response.status_code, 200)


class AdminServiceViewTests(TestCase):
    def test_get_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 403)

    def test_get_not_super_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 403)

    def test_get_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 200)

    def test_post_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.post(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 403)

    def test_post_not_super_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.post(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 403)

    def test_post_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        response = client.post(reverse("app:admin_service"))
        self.assertEquals(response.status_code, 200)

    def test_post_service_addition_form(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        params = {
            "service_name": "test_service",
            "api_server_url": "localhost:9999",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:admin_service"), params)
        self.assertEquals(response.status_code, 200)
        service = Service.objects.get(name=params["service_name"])
        workflows = Workflow.objects.filter(
            service__name=params["service_name"])
        self.assertIsNotNone(service)
        self.assertIsNotNone(workflows)

    def test_post_service_addition_form_error(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        params = {
            "service_name": "test_service",
            "api_server_url": "localhost:9998",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:admin_service"), params)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Please enter the correct URL.")

    def test_post_duplicate_service(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.is_superuser = True
        user.save()
        client.force_login(user)
        params = {
            "service_name": "test_service",
            "api_server_url": "localhost:9999",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:admin_service"), params)
        self.assertEquals(response.status_code, 200)
        params = {
            "service_name": "test_service",
            "api_server_url": "localhost:9999",
            "button_add_service": "submit",
        }
        response = client.post(reverse("app:admin_service"), params)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "A form with that name already exists.")
