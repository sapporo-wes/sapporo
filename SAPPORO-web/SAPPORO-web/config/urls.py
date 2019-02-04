# coding: utf-8
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from .settings import DEBUG

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path("", include("app.urls")),
]


if DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
