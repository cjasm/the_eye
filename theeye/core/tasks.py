from theeye.core.models import Error
from theeye.core.serializers import EventSerializer
from celery import shared_task


@shared_task
def event_handler(payload):
    for data in payload:
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            error_msg = serializer.errors['data'][0]
            Error(message=error_msg, data=data).save()
