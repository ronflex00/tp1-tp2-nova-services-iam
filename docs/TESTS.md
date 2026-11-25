# Tests

Lancer `bash scripts/verify.sh`. Il contrôle Docker, Python, la configuration, les quatre services, PostgreSQL (`SELECT 1`), les endpoints live/ready Authentik, le worker et l'API Grafana.

Commandes manuelles :

```bash
docker compose exec postgres sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 AS test;"'
curl -i http://localhost:9000/-/health/live/
curl -i http://localhost:9000/-/health/ready/
docker compose exec authentik-worker ak healthcheck
curl -fsS http://localhost:3000/api/health | python3 -m json.tool
```

La liveness indique que le processus répond. La readiness indique que le service est prêt à recevoir du trafic et que ses dépendances sont disponibles. Un code HTTP 200 est attendu pour les deux endpoints ; Grafana doit notamment retourner `"database": "ok"`.

Contrôle du 25 novembre 2026 : les quatre services sont healthy et tous les contrôles ci-dessus sont PASS. Le port 9000 est utilisé par ce laboratoire. Voir [la recette finale](RECETTE_FINALE.md).

