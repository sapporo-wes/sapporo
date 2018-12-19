# coding: utf-8
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("app.urls")),
    path('django-admin/', admin.site.urls),
]
