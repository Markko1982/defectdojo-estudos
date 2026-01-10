from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from dojo.models import Finding


class FindingHasEndpointsFilterTest(APITestCase):
    """Tests for /api/v2/findings/?has_endpoints=true|false"""

    fixtures = ["dojo_testdata.json"]

    def setUp(self):
        token = Token.objects.get(user__username="admin")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def _list(self, **params):
        # Dojo usa LimitOffsetPagination (PAGE_SIZE=25). Pegamos tudo numa página só.
        params.setdefault("limit", 1000)
        return self.client.get(reverse("finding-list"), params)

    def test_has_endpoints_true(self):
        r = self._list(has_endpoints="true")
        self.assertEqual(r.status_code, 200, r.content[:1000])

        results = r.json()["results"]
        self.assertGreaterEqual(len(results), 1, r.content[:1000])

        ids = [item["id"] for item in results]
        self.assertEqual(
            Finding.objects.filter(id__in=ids, endpoints__isnull=True)
            .distinct()
            .count(),
            0,
            "Retornou finding sem endpoints com has_endpoints=true",
        )

    def test_has_endpoints_false(self):
        r = self._list(has_endpoints="false")
        self.assertEqual(r.status_code, 200, r.content[:1000])

        results = r.json()["results"]
        self.assertGreaterEqual(len(results), 1, r.content[:1000])

        ids = [item["id"] for item in results]
        self.assertEqual(
            Finding.objects.filter(id__in=ids, endpoints__isnull=False)
            .distinct()
            .count(),
            0,
            "Retornou finding com endpoints com has_endpoints=false",
        )
