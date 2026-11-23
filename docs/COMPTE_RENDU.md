# TP1 — Installation de l'infrastructure IAM

## 1. Contexte

Nova Services. Gitea n'a pas été retenu ; le périmètre comprend PostgreSQL, Authentik Server, Authentik Worker et Grafana.

## 2. Objectifs

Déployer une base IAM persistante avec Docker Compose, secrets locaux protégés, healthchecks et préparation du futur SSO OIDC.

## 3. Architecture

Voir `docs/ARCHITECTURE.md`. PostgreSQL est interne, Authentik écoute sur 9000 et Grafana sur 3000.

## 4. Services installés

Les versions et rôles sont documentés dans `README.md`.

## 5. Gestion des secrets

`scripts/init_env.py` génère `.env` une seule fois avec `secrets.token_hex`, droits 0600 et refus d'écrasement. `.env` est exclu de Git.

## 6. Installation

Voir `docs/INSTALLATION.md`.

## 7. Vérifications

Résultats réels à compléter après démarrage. `scripts/verify.sh` fournit la recette automatisée.

## 8. Initialisation Authentik

À effectuer manuellement sur `http://localhost:9000/if/flow/initial-setup/` avec le compte `akadmin`. Ne pas placer son mot de passe dans un fichier du projet.

## 9. Initialisation Grafana

À effectuer sur `http://localhost:3000` avec `admin` et la valeur locale de `GRAFANA_ADMIN_PASSWORD`.

## 10. Test de persistance

Voir `docs/PERSISTENCE.md`. À réaliser après initialisation ; aucune capture fictive n'est fournie.

## 11. Sécurité

PostgreSQL n'est pas publié, aucun socket Docker n'est monté, aucun `privileged: true` ni `chmod -R 777` n'est utilisé. Les secrets ne sont pas écrits dans Compose ni dans les fichiers suivis.

## 12. Conclusion

Le socle TP1 est préparé. Le SSO Authentik/Grafana est réservé au TP2.

Captures à insérer :

- [CAPTURE 1 — docker compose ps]
- [CAPTURE 2 — Administration Authentik]
- [CAPTURE 3 — Grafana]
- [CAPTURE 4 — Groupe tp1-persistence avant redémarrage]
- [CAPTURE 5 — Groupe tp1-persistence après redémarrage]

