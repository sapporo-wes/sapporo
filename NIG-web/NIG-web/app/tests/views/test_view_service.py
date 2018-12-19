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
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:service_list"))
        self.assertEquals(response.status_code, 200)


class ServiceDetailViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:service_detail", kwargs={
            "service_name": "service_name"}))
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        service = Service()
        service.name = "test_service"
        service.save()
        response = client.get(reverse("app:service_detail", kwargs={
            "service_name": "test_service"}))
        self.assertEquals(response.status_code, 200)

    def test_not_exists(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:service_detail", kwargs={
            "service_name": "test_service"}))
        self.assertEquals(response.status_code, 404)
