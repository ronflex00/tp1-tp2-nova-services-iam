# Installation

1. Vérifier les ports : `docker ps --format "table {{.Names}}\t{{.Ports}}"`.
2. Générer une seule fois les secrets avec `python3 scripts/init_env.py`.
3. Télécharger les images avec `docker compose pull`.
4. Préparer les permissions avec la commande documentée dans le README.
5. Démarrer avec `docker compose up -d --wait --wait-timeout 600`.

Le démarrage est conditionné à la santé de PostgreSQL. Le port 9000 doit être libre ; dans l'environnement de réalisation, il est actuellement occupé par un autre projet SonarQube.

