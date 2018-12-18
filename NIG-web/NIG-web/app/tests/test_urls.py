# coding: utf-8
from django.test import TestCase
from django.urls import resolve, reverse


class UrlResolveTests(TestCase):
    def test_url_resolves_to_home_view(self):
        resolver = resolve("/")
        self.assertEqual(resolver.view_name, "app:home")

    def test_url_resolves_to_signin_view(self):
        resolver = resolve("/signin/")
        self.assertEqual(resolver.view_name, "app:signin")

    def test_url_resolves_to_signout_view(self):
        resolver = resolve("/signout/")
        self.assertEqual(resolver.view_name, "app:signout")

    def test_url_resolves_to_signup_view(self):
        resolver = resolve("/signup/")
        self.assertEqual(resolver.view_name, "app:signup")

    def test_url_resolves_to_service_list_view(self):
        resolver = resolve("/service/")
        self.assertEqual(resolver.view_name, "app:service_list")

    def test_url_resolves_to_job_list_view(self):
        resolver = resolve("/job/")
        self.assertEqual(resolver.view_name, "app:job_list")

    def test_url_resolves_to_data_list_view(self):
        resolver = resolve("/data/")
        self.assertEqual(resolver.view_name, "app:data_list")

    def test_url_resolves_to_user_detai_view(self):
        resolver = resolve("/user/test_user/")
        self.assertEqual(resolver.view_name, "app:user_detail")
        self.assertEqual(resolver.kwargs["user_name"], "test_user")


class UrlReverseTests(TestCase):
    def test_reverse_home(self):
        url = reverse("app:home")
        self.assertEqual(url, "/")

    def test_reverse_signin(self):
        url = reverse("app:signin")
        self.assertEqual(url, "/signin/")

    def test_reverse_signout(self):
        url = reverse("app:signout")
        self.assertEqual(url, "/signout/")

    def test_reverse_signup(self):
        url = reverse("app:signup")
        self.assertEqual(url, "/signup/")

    def test_reverse_service_list(self):
        url = reverse("app:service_list")
        self.assertEqual(url, "/service/")

    def test_reverse_job_list(self):
        url = reverse("app:job_list")
        self.assertEqual(url, "/job/")

    def test_reverse_data_list(self):
        url = reverse("app:data_list")
        self.assertEqual(url, "/data/")

    def test_reverse_user_detai(self):
        url = reverse("app:user_detail", kwargs={"user_name": "test_user"})
        self.assertEqual(url, "/user/test_user/")
