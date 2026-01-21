import json

from django.test import TestCase


class TestPingAnonymous(TestCase):
    def test_ping_is_public_and_returns_ok(self):
        response = self.client.get("/ping")

        assert response.status_code == 200
        assert response["Content-Type"].split(";")[0] == "application/json"

        data = json.loads(response.content.decode("utf-8"))
        assert data == {"status": "ok"}

    def test_ping_post_not_allowed(self):
        response = self.client.post("/ping")
        assert response.status_code == 405
