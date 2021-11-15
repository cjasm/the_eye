from rest_framework.test import APITestCase
from theeye.core.models import Event


class EventGet(APITestCase):

    def setUp(self):
        self.data = [
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                },
                "timestamp": "2021-01-01 09:15:27.243860"
            },
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "cta click",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "element": "chat bubble"
                },
                "timestamp": "2021-01-01 09:15:27.243860"
            },
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "form interaction",
                "name": "submit",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "form": {
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                },
                "timestamp": "2021-01-01 09:15:27.243860"
            },
            {
                "session_id": "aaaaaa-aaaa-aaaaaa-aaaa",
                "category": "page interaction",
                "name": "cta click",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "element": "chat bubble"
                },
                "timestamp": "2021-01-02 09:15:27.243860"
            }
        ]
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
        response = self.client.get('/api/events/?date-from=2021-01-01 09:15:27.243860&date-to=2021-01-01 09:15:27.243860')
        self.assertEqual(len(response.data), 3)

    def test_filter_by_category(self):
        response = self.client.get('/api/events/?session=aaaaaa-aaaa-aaaaaa-aaaa')
        self.assertEqual(len(response.data), 1)
