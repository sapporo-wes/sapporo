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

    def test_url_resolves_to_admin_view(self):
        resolver = resolve("/admin/")
        self.assertEqual(resolver.view_name, "app:admin_home")

    def test_url_resolves_to_admin_service_view(self):
        resolver = resolve("/admin/services/")
        self.assertEqual(resolver.view_name, "app:admin_service")

    def test_url_resolves_to_service_list_view(self):
        resolver = resolve("/services/")
        self.assertEqual(resolver.view_name, "app:service_list")

    def test_url_resolves_to_service_detail_view(self):
        resolver = resolve("/services/service_name/")
        self.assertEqual(resolver.view_name, "app:service_detail")
        self.assertEqual(resolver.kwargs["service_name"], "service_name")

    def test_url_resolves_to_workflow_list_view(self):
        resolver = resolve("/workflows/")
        self.assertEqual(resolver.view_name, "app:workflow_list")

    def test_url_resolves_to_workflow_detail_view(self):
        resolver = resolve("/workflows/workflow_unique_id/")
        self.assertEqual(resolver.view_name, "app:workflow_detail")
        self.assertEqual(
            resolver.kwargs["workflow_unique_id"], "workflow_unique_id")

    def test_url_resolves_to_run_list_view(self):
        resolver = resolve("/runs/")
        self.assertEqual(resolver.view_name, "app:run_list")

    def test_url_resolves_to_run_detail_view(self):
        resolver = resolve("/runs/run_unique_id/")
        self.assertEqual(resolver.view_name, "app:run_detail")
        self.assertEqual(
            resolver.kwargs["run_unique_id"], "run_unique_id")

    def test_url_resolves_to_data_list_view(self):
        resolver = resolve("/data/")
        self.assertEqual(resolver.view_name, "app:data_list")

    def test_url_resolves_to_data_detail_view(self):
        resolver = resolve("/data/data_unique_id/")
        self.assertEqual(resolver.view_name, "app:data_detail")
        self.assertEqual(
            resolver.kwargs["data_unique_id"], "data_unique_id")

    def test_url_resolves_to_user_detai_view(self):
        resolver = resolve("/test_user/")
        self.assertEqual(resolver.view_name, "app:user_home")
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

    def test_reverse_admin(self):
        url = reverse("app:admin_home")
        self.assertEqual(url, "/admin/")

    def test_reverse_admin_service(self):
        url = reverse("app:admin_service")
        self.assertEqual(url, "/admin/services/")

    def test_reverse_service_list(self):
        url = reverse("app:service_list")
        self.assertEqual(url, "/services/")

    def test_reverse_service_detail(self):
        url = reverse("app:service_detail", kwargs={
                      "service_name": "service_name"})
        self.assertEqual(url, "/services/service_name/")

    def test_reverse_workflow_list(self):
        url = reverse("app:workflow_list")
        self.assertEqual(url, "/workflows/")

    def test_reverse_workflow_detail(self):
        url = reverse("app:workflow_detail", kwargs={
                      "workflow_unique_id": "workflow_unique_id"})
        self.assertEqual(url, "/workflows/workflow_unique_id/")

    def test_reverse_run_list(self):
        url = reverse("app:run_list")
        self.assertEqual(url, "/runs/")

    def test_reverse_run_detail(self):
        url = reverse("app:run_detail", kwargs={
                      "run_unique_id": "run_unique_id"})
        self.assertEqual(url, "/runs/run_unique_id/")

    def test_reverse_data_list(self):
        url = reverse("app:data_list")
        self.assertEqual(url, "/data/")

    def test_reverse_data_detail(self):
        url = reverse("app:data_detail", kwargs={
                      "data_unique_id": "data_unique_id"})
        self.assertEqual(url, "/data/data_unique_id/")

    def test_reverse_user_detai(self):
        url = reverse("app:user_home", kwargs={"user_name": "test_user"})
        self.assertEqual(url, "/test_user/")
