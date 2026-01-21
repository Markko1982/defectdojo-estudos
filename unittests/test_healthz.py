import json
from unittest.mock import MagicMock, patch

from django.db import DatabaseError
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
    
    def test_healthz_post_not_allowed(self):
        response = self.client.post("/healthz")
        assert response.status_code == 405


    def test_home_still_requires_login(self):
        # A home continua protegida -> redireciona pro login
        response = self.client.get("/", follow=False)

        assert response.status_code == 302
        assert response["Location"].startswith("/login")
        
    @patch("dojo.health.connections")
    def test_healthz_db_error_returns_503(self, connections_mock):
        # Monta um "fake" para connections["default"].cursor().__enter__().execute(...)
        conn = MagicMock()
        connections_mock.__getitem__.return_value = conn

        cursor_cm = MagicMock()
        conn.cursor.return_value = cursor_cm

        cursor = MagicMock()
        cursor_cm.__enter__.return_value = cursor

        # Simula falha na hora de executar a query
        cursor.execute.side_effect = DatabaseError("db down")

        response = self.client.get("/healthz")

        assert response.status_code == 503

        data = json.loads(response.content.decode("utf-8"))
        assert data == {"status": "degraded", "reason": "db"}
