from django.db import models
from django.utils import timezone


class JobExecution(models.Model):
    job_id = models.IntegerField(null=False, blank=False)
    job_name = models.CharField(null=True, blank=True, max_length=50)
    author = models.CharField(null=True, blank=True, max_length=50)
    start_time = models.DateTimeField(default=timezone.now(), blank=True)
    end_time = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    status = models.CharField(max_length=30)
    progress = models.CharField(max_length=100, null=True, blank=True)

