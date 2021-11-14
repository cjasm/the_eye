from rest_framework import viewsets
from rest_framework.response import Response
from theeye.core.models import Event
from theeye.core.serializers import EventSerializer


class EventViewSet(viewsets.ViewSet):
    """
    This Viewset should deal with Event list, creation, retrieve and update
    """

    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
