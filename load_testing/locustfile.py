import random

from locust import FastHttpUser, task
from locust.user.wait_time import between
from sklearn.datasets import fetch_20newsgroups

categories = [
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey",
]
data = fetch_20newsgroups(subset="test", categories=categories)


class QueryModel(FastHttpUser):
    host = "http://127.0.0.1:30010"
    wait_time = between(0.1, 0.2)

    @task
    def stats(self):
        self.client.post("/predict", data=random.choice(data.data))
