from rest_framework import serializers
from theeye.core.models import Event, Error
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):

    def validate_data(self, value):
        """
        Validates if data is not empty and if it has host and path attribute
        """
        if not value:
            raise serializers.ValidationError("Event payload data invalid")
        if any(key not in value.keys() for key in ('host', 'path')):
            raise serializers.ValidationError("Event payload data is missing host and path")
        return value

    def validate_timestamp(self, value):
        """
        Validates if time is not from the future
        """
        if value > timezone.now():
            raise serializers.ValidationError("Event timestamp is invalid")
        return value

    class Meta:
        model = Event
        exclude = ['created_at']


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = '__all__'
