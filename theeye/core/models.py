from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Event(BaseModel):
    session_id = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    data = models.JSONField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']


class Error(BaseModel):
    message = models.CharField(max_length=50)
    data = models.JSONField()

    class Meta:
        ordering = ['-created_at']