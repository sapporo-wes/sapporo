# coding: utf-8
from app.views import (AdminHomeView, AdminServiceView, HomeView,
                       RunDetailView, RunListView, ServiceDetailView,
                       ServiceListView, SignupView, UserHomeView,
                       WorkflowDetailView, WorkflowListView,
                       WorkflowPreparationView)
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

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
         ServiceDetailView.as_view(), name="service_detail"),
    path("workflows/", WorkflowListView.as_view(), name="workflow_list"),
    path("workflows/<slug:workflow_token>/",
         WorkflowDetailView.as_view(), name="workflow_detail"),
    path("workflows/<slug:workflow_token>/preparation",
         WorkflowPreparationView.as_view(), name="workflow_preparation"),
    path("runs/", RunListView.as_view(), name="run_list"),
    path("runs/<slug:run_token>/",
         RunDetailView.as_view(), name="run_detail"),
    path("<str:user_name>/", UserHomeView.as_view(), name="user_home"),
]
