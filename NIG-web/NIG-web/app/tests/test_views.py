from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import Service


class HomeViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:home"))
        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:home"))
        self.assertEquals(response.status_code, 200)


class SigninViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:signin"))
        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
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
        user.username = "TestUser"
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
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:signup"))
        self.assertEquals(response.status_code, 200)


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


class JobListViewTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get(reverse("app:job_list"))
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        response = client.get(reverse("app:job_list"))
        self.assertEquals(response.status_code, 200)


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


class UserDetailTests(TestCase):
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        url = reverse("app:user_detail", kwargs={"user_name": "TestUser"})
        response = client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_authenticated(self):
        client = Client()
        user = User()
        user.username = "TestUser"
        user.save()
        client.force_login(user)
        url = reverse("app:user_detail", kwargs={"user_name": user.username})
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("user" in response.context)
        self.assertEqual(user, response.context['user'])
