# coding: utf-8
from django.contrib import admin
from app.models import Service
from app.models import WorkflowEngine
from app.models import WorkflowTypeVersion
from app.models import SupportedWesVersion
from app.models import SupportedFilesystemProtocol
from app.models import SystemStateCount
from app.models import Run

admin.site.register(Service)
admin.site.register(WorkflowEngine)
admin.site.register(WorkflowTypeVersion)
admin.site.register(SupportedWesVersion)
admin.site.register(SupportedFilesystemProtocol)
admin.site.register(SystemStateCount)
admin.site.register(Run)
