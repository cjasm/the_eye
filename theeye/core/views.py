from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from theeye.core.models import Event, Error
from theeye.core.serializers import EventSerializer, ErrorSerializer
from theeye.core.tasks import event_handler


class EventViewSet(viewsets.ViewSet):
    """
    This Viewset should deal with Event list and creation
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
        """
        Sends the creation responsability to the background task 'event_handler'
        """
        data = request.data
        if not data or type(data) != list:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "the request data is invalid"})

        task = event_handler.delay(data)
        return Response(data={'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class ErrorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer
