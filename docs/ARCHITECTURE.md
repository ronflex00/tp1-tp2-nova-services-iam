# Architecture

```text
Navigateur ── http://localhost:9000 ── Authentik Server ── PostgreSQL
                                      └─ Authentik Worker
Navigateur ── http://localhost:3000 ── Grafana
```

Tous les services sont sur `iam-network`. PostgreSQL n'expose aucun port sur l'hôte. Les volumes `postgres_data`, `grafana_data` et le répertoire `data/authentik` séparent les données du cycle de vie des conteneurs.

Versions : PostgreSQL 16-alpine, Authentik 2026.8.6, Grafana 13.3.1. Gitea est volontairement absent.

