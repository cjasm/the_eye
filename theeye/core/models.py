from django.db import models


class Event(models.Model):
    session_id = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Error(models.Model):
    message = models.CharField(max_length=50)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
