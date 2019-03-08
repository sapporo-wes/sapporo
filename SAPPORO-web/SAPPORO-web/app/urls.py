# coding: utf-8
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from app.views import (AdminHomeView, AdminServiceView, HomeView,
                       LoginNoPlaceholderView, RunDetailView, RunDownloadView,
                       RunListView, ServiceDetailView, ServiceListView,
                       SignupView, UserHomeView, WorkflowDetailView,
                       WorkflowListView, WorkflowPrepareView)

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signin/", LoginNoPlaceholderView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),
    path("admin/", AdminHomeView.as_view(), name="admin_home"),
    path("admin/services/", AdminServiceView.as_view(), name="admin_service"),
    path("runs/", RunListView.as_view(), name="run_list"),
    path("runs/<slug:run_id>/", RunDetailView.as_view(), name="run_detail"),
    path("runs/<slug:run_id>/download",
         RunDownloadView.as_view(), name="run_download"),
    path("services/", ServiceListView.as_view(), name="service_list"),
    path("services/<str:service_name>/",
         ServiceDetailView.as_view(), name="service_detail"),
    path("workflows/", WorkflowListView.as_view(), name="workflow_list"),
    path("workflows/<slug:workflow_token>/",
         WorkflowDetailView.as_view(), name="workflow_detail"),
    path("workflows/<slug:workflow_token>/prepare",
         WorkflowPrepareView.as_view(), name="workflow_prepare"),
]

if settings.ENABLE_USER_SIGNUP:
    urlpatterns.insert(2, path("signup/", SignupView.as_view(), name="signup"))
