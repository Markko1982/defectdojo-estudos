import json

from django.test import TestCase


class TestHealthzAnonymous(TestCase):
    def test_healthz_is_public_and_returns_ok(self):
        # request anônimo (sem login/cookie)
        response = self.client.get("/healthz")

        assert response.status_code == 200
        # em Django, JsonResponse normalmente vem como application/json
        assert response["Content-Type"].split(";")[0] == "application/json"

        data = json.loads(response.content.decode("utf-8"))
        assert data == {"status": "ok"}

    def test_home_still_requires_login(self):
        # A home continua protegida -> redireciona pro login
        response = self.client.get("/", follow=False)

        assert response.status_code == 302
        assert response["Location"].startswith("/login")
