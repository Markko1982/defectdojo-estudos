# Onboarding - Debug local (DefectDojo)

## Ver serviços rodando
```bash
docker compose ps

---

## Ver logs do Celery (tarefas assíncronas)
O Celery roda “trabalhos em background” (imports, notificações, jobs agendados). Quando algo “some” e não aparece no Django, muitas vezes está aqui.

```bash
docker compose logs -f --tail=100 celeryworker
