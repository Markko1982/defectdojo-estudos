from django.db import DatabaseError, connections
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "degraded", "reason": "db"}, status=503)

    return JsonResponse({"status": "ok"}, status=200)

@require_GET
def ping(request):
    # Endpoint simples para checar se o serviço está respondendo (sem depender do DB).
    return JsonResponse({"status": "ok"}, status=200)

