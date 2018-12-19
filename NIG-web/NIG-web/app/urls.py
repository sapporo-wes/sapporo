# coding: utf-8
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app.views import (AdminHomeView, AdminServiceView, DataDetailView,
                    DataListView, HomeView, RunDetailView, RunListView,
                    ServiceDetailView, ServiceListView, SignupView,
                    UserHomeView, WorkflowListView, WorkflowDetailView)

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signin/", LoginView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("admin/", AdminHomeView.as_view(), name="admin_home"),
    path("admin/services/", AdminServiceView.as_view(), name="admin_service"),
    path("services/", ServiceListView.as_view(), name="service_list"),
    path("services/<str:service_name>/",
         ServiceListView.as_view(), name="service_detail"),
    path("workflows/", WorkflowListView.as_view(), name="workflow_list"),
    path("workflows/<slug:workflow_unique_id>/",
         WorkflowListView.as_view(), name="workflow_detail"),
    path("runs/", RunListView.as_view(), name="run_list"),
    path("runs/<slug:run_unique_id>/",
         RunDetailView.as_view(), name="run_detail"),
    path("data/", DataListView.as_view(), name="data_list"),
    path("data/<slug:data_unique_id>/",
         DataDetailView.as_view(), name="data_detail"),
    path("<str:user_name>/", UserHomeView.as_view(), name="user_home"),
]
