import uuid
from django.db import models

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    desc_1 = models.TextField(blank=True, null=True)
    desc_2 = models.TextField(blank=True, null=True)
    desc_3 = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.school_name