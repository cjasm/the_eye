from locust import HttpUser, TaskSet, task, between
from theeye.core.utils import Fixture
import json


class LoadTest(TaskSet):
    def on_start(self):
        self.data = json.dumps(Fixture().event_data)

    @task
    def send_events(self):
        self.client.post('/api/events/', data=self.data, headers={'Content-Type': 'application/json'})


class MainClassTest(HttpUser):
    tasks = [LoadTest]
    wait_time = between(5, 10)
