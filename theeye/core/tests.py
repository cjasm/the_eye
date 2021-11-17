from django.test import TestCase
from rest_framework.test import APITestCase
from celery.result import AsyncResult
from theeye.core.models import Event, Error
from theeye.core.serializers import EventSerializer
from theeye.core.utils import Fixture
from theeye.core.tasks import event_handler


class EventGet(APITestCase):

    def setUp(self):
        self.data = Fixture().event_data
        for event in self.data:
            Event.objects.create(**event)
        self.resp = self.client.get('/api/events/')

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_has_event(self):
        self.assertEqual(len(self.resp.data), 4)

    def test_filter_by_category(self):
        response = self.client.get('/api/events/?category=form%20interaction')
        self.assertEqual(len(response.data), 1)

    def test_filter_by_time_range(self):
        response = self.client.get(
            '/api/events/?date-from=2021-01-01 09:15:27.243860&date-to=2021-01-01 09:15:27.243860')
        self.assertEqual(len(response.data), 3)

    def test_filter_by_session(self):
        response = self.client.get('/api/events/?session=aaaaaa-aaaa-aaaaaa-aaaa')
        self.assertEqual(len(response.data), 1)


class EventPostValid(APITestCase):

    def setUp(self):
        self.data = Fixture().event_error_data
        self.resp = self.client.post('/api/events/', self.data, format='json')

    def test_post(self):
        self.assertEqual(self.resp.status_code, 202)

    def test_has_event_in_processing(self):
        task_id = self.resp.data['task_id']
        self.assertFalse(AsyncResult(task_id).failed())


class EventPostInvalid(APITestCase):

    def setUp(self):
        self.data = Fixture().invalid_data
        self.resp = self.client.post('/api/events/', self.data, format='json')

    def test_post(self):
        self.assertEqual(self.resp.status_code, 400)

    def test_error_msg(self):
        self.assertEqual(self.resp.data['message'], "the request data is invalid")

    def test_post_empty_data(self):
        data = Fixture().empty_data
        resp = self.client.post('/api/events/', data, format='json')
        self.assertEqual(resp.status_code, 400)


class ErrorGet(APITestCase):
    def setUp(self):
        data = Fixture().event_error_data[0]
        serializer = EventSerializer(data=data)
        serializer.is_valid()
        Error(message=serializer.errors['data'][0], data=data).save()
        self.resp = self.client.get('/api/errors/')

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_has_errors(self):
        self.assertGreaterEqual(self.resp.data['count'], 1)


class ErrorPost(APITestCase):
    def setUp(self):
        self.data = Fixture().event_data
        self.resp = self.client.post('/api/errors/', self.data, format='json')

    def test_post(self):
        self.assertEqual(self.resp.status_code, 405)


class CeleryTest(TestCase):
    def setUp(self):
        self.task = event_handler.delay(Fixture().event_error_data)

    def test_background_task(self):
        self.task.get()
        self.assertTrue(self.task.successful())
