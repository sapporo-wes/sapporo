# coding: utf-8
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class RunListViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:run_list"))
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:run_list"))
        self.assertEquals(response.status_code, 200)


class RunDetailViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:run_detail", kwargs={
            "run_unique_id": "run_unique_id"}))
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "test_user"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:run_detail", kwargs={
            "run_unique_id": "run_unique_id"}))
        self.assertEquals(response.status_code, 200)
