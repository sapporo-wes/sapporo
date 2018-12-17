# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    name = models.CharField(_("Service name"), max_length=256)
    api_server_url = models.CharField(_("API server url"), max_length=256)
    auth_instructions_url = models.CharField(
        _("Auth instructions url"), max_length=256)
    contact_info_url = models.CharField(_("Contact info url"), max_length=256)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "service"
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self):
        return "Service: {}".format(self.name)


class WorkflowEngine(models.Model):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    name = models.CharField(_("Workflow engine name"), max_length=64)
    version = models.CharField(_("Workflow engine version"), max_length=64)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "workflow_engine"
        verbose_name = "workflow_engine"
        verbose_name_plural = "workflow_engines"

    def __str__(self):
        return "Workflow Engine: {}".format(self.name)


class WorkflowTypeVersion(models.Model):
    workflow_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Belong workflow engine"), on_delete=models.CASCADE)
    type_version = models.CharField(_("Workflow type version"), max_length=64)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "workflow_type_version"
        verbose_name = "workflow_type_version"
        verbose_name_plural = "workflow_type_versions"

    def __str__(self):
        return "Workflow Type Version: {}".format(self.type_version)


class SupportedWesVersion(models.Model):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    wes_version = models.CharField(_("Wes version"), max_length=64)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "supported_wes_version"
        verbose_name = "supported_wes_version"
        verbose_name_plural = "supported_wes_versions"

    def __str__(self):
        return "Supported Wes Version: {}".format(self.wes_version)


class SupportedFilesystemProtocol(models.Model):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    name = models.CharField(_("Filesystem Protocol name"), max_length=64)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "supported_filesystem_protocol"
        verbose_name = "supported_filesystem_protocol"
        verbose_name_plural = "supported_filesystem_protocols"

    def __str__(self):
        return "Supported Filesystem Protocol: {}".format(self.name)


class DefaultWorkflowEngineParameter(models.Model):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    key = models.CharField(_("Parameter key"), max_length=64)
    value = models.CharField(_("Parameter value"), max_length=64)
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "default_workflow_engine_parameter"
        verbose_name = "default_workflow_engine_parameter"
        verbose_name_plural = "default_workflow_engine_parameters"

    def __str__(self):
        return "Default Workflow Engine Parameter: {}, {}".format(self.key, self.value)


class SystemStateCount(models.Model):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    state = models.CharField(_("System state"), max_length=64)
    count = models.IntegerField(_("Counte"))
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        db_table = "system_state_count"
        verbose_name = "system_state_count"
        verbose_name_plural = "system_state_counts"

    def __str__(self):
        return "System State Count: {}, {}".format(self.state, str(self.count))
