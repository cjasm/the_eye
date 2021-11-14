from rest_framework.test import APITestCase
from theeye.core.models import Event


class EventGet(APITestCase):

    def setUp(self):
        self.data = {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        }
        Event.objects.create(**self.data)
        self.resp = self.client.get('/api/events/')

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_has_event(self):
        self.assertEqual(len(self.resp.data), 1)
