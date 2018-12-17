# coding: utf-8
from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Job(models.Model):
    name = models.CharField(_("job name"), max_length=256)
    user = models.ForeignKey(User, verbose_name=_(
        "executing user"), on_delete=models.CASCADE)
    workflow = models.CharField(_("workflow name"), max_length=256)
    status = models.CharField(_("status"), max_length=64)
    date_created = models.DateTimeField(
        _("date created"), default=timezone.now)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    config_file_path = models.CharField(_("config file path"), max_length=256)

    class Meta:
        db_table = "job"
        verbose_name = "job"
        verbose_name_plural = "jobs"

    def __str__(self):
        return self.name
