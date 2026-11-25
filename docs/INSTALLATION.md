# Installation

1. Vérifier les ports : `docker ps --format "table {{.Names}}\t{{.Ports}}"`.
2. Générer une seule fois les secrets avec `python3 scripts/init_env.py`.
3. Télécharger les images avec `docker compose pull`.
4. Préparer les permissions avec la commande documentée dans le README.
5. Démarrer avec `docker compose up -d --wait --wait-timeout 600`.

Le démarrage est conditionné à la santé de PostgreSQL. Les ports hôte 9000 et 3000 doivent être libres avant la première installation ; ils sont actuellement utilisés par ce laboratoire.

## Reprise et amorçage TP2

Sur le laboratoire existant, conserver le fichier .env, les volumes et les comptes, puis utiliser la commande de reprise du [README](../README.md).

Le Compose livré correspond à l'état final TP2 : il exige aussi GRAFANA_OIDC_CLIENT_ID et GRAFANA_OIDC_CLIENT_SECRET. Le script init_env.py génère uniquement les trois secrets TP1. Les cinq étapes ci-dessus ne suffisent donc pas seules sur un poste vierge : préparer d'abord un démarrage TP1 avec OAuth non activé, initialiser Authentik et le provider suivant [oidc.md](oidc.md), puis renseigner localement les variables OIDC avant de démarrer le Compose final. Cette phase d'amorçage n'a pas été rejouée lors de la recette du rendu.

