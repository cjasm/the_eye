from rest_framework import serializers
from theeye.core.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_at']
