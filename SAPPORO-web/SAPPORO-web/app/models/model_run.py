# # coding: utf-8
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _

# from app.models import Service, WorkflowEngine, WorkflowType


# class CommonInfo(models.Model):
#     created_at = models.DateTimeField(_("Created date"), default=timezone.now)
#     updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

#     class Meta:
#         abstract = True


# class Run(CommonInfo):
#     name = models.CharField(_("Run name"), max_length=256)
#     user = models.ForeignKey(User, verbose_name=_(
#         "Executing user"), on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, verbose_name=_(
#         "Executing service"), on_delete=models.CASCADE)
#     id_in_service = models.IntegerField(_("ID in service"))
#     status = models.CharField(_("Status"), max_length=64)
#     workflow_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
#         "Workflow engine"), on_delete=models.CASCADE)
#     workflow_type_version = models.ForeignKey(WorkflowType, verbose_name=_(
#         "Workflow type version"), on_delete=models.CASCADE)

#     class Meta:
#         db_table = "run"
#         verbose_name = "run"
#         verbose_name_plural = "runs"

#     def __str__(self):
#         return "Run: {}".format(self.name)


# class Log(CommonInfo):
#     name = models.CharField(_("Log name"), max_length=256)
#     run = models.ForeignKey(Run, verbose_name=_(
#         "Run"), on_delete=models.CASCADE)
#     start_time = models.DateTimeField(_("Start time"))
#     end_time = models.DateTimeField(_("End time"))
#     stdout = models.TextField(_("Stdout"))
#     stderr = models.TextField(_("Stderr"))
#     exit_code = models.IntegerField(_("Exit code"))

#     class Meta:
#         db_table = "log"
#         verbose_name = "log"
#         verbose_name_plural = "logs"

#     def __str__(self):
#         return "Log: {}".format(self.name)


# class Command(CommonInfo):
#     log = models.ForeignKey(Log, verbose_name=_("Log"),
#                             on_delete=models.CASCADE)
#     cmd = models.CharField(_("Command"), max_length=256)

#     class Meta:
#         db_table = "command"
#         verbose_name = "command"
#         verbose_name_plural = "commands"

#     def __str__(self):
#         return "Command: {}".format(self.id)
