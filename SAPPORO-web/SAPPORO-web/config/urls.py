# coding: utf-8
from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("app.urls")),
]


if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
