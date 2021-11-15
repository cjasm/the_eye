from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.response import Response
from theeye.core.models import Event, Error
from theeye.core.serializers import EventSerializer, ErrorSerializer


class EventViewSet(viewsets.ViewSet):
    """
    This Viewset should deal with Event list, creation, retrieve and update
    """

    def list(self, request):
        queryset = Event.objects.all()
        date_from_query = request.query_params.get('date-from', None)
        date_to_query = request.query_params.get('date-to', None)
        category_query = request.query_params.get('category', None)
        session_query = request.query_params.get('session', None)

        if date_from_query and date_to_query:
            date_from_query, date_to_query = parse_datetime(date_from_query), parse_datetime(date_to_query)
            queryset = queryset.filter(timestamp__range=(date_from_query, date_to_query))
        if category_query:
            queryset = queryset.filter(category=category_query)
        if session_query:
            queryset = queryset.filter(session_id=session_query)

        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        for data in request.data:
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                Error(message=serializer.errors['data'][0], data=data).save()

        return Response()


class ErrorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer
