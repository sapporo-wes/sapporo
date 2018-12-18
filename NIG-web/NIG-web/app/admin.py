# coding: utf-8
from django.contrib import admin
from .models import Service
from .models import WorkflowEngine
from .models import WorkflowTypeVersion
from .models import SupportedWesVersion
from .models import SupportedFilesystemProtocol
# from .models import DefaultWorkflowEngineParameter
from .models import SystemStateCount
from .models import Run

admin.site.register(Service)
admin.site.register(WorkflowEngine)
admin.site.register(WorkflowTypeVersion)
admin.site.register(SupportedWesVersion)
admin.site.register(SupportedFilesystemProtocol)
# admin.site.register(DefaultWorkflowEngineParameter)
admin.site.register(SystemStateCount)
admin.site.register(Run)
