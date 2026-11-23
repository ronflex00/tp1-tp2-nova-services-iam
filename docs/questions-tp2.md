# Questions TP2 — réponses

1. L'identité décrit le sujet ; l'authentification vérifie cette identité ; l'autorisation décide des actions permises.
2. `role` est un attribut métier. Un droit doit être accordé explicitement par groupe, policy, provider ou application.
3. Un Admin Grafana administre Grafana, pas toute la configuration Authentik. La séparation limite l'impact d'une compromission.
4. Grafana Admin est un rôle d'organisation ; `GrafanaAdmin` est un rôle serveur global plus puissant.
5. Editor est un rôle large au niveau organisation. Une permission de dossier explicite est nécessaire pour limiter finement l'accès.
6. Retirer les anciens droits lors d'une mobilité évite l'accumulation de privilèges.
7. Enrôler TOTP associe un facteur à l'utilisateur ; imposer MFA exige ce facteur dans le parcours de connexion.
8. TOTP réduit le risque lié au seul mot de passe, mais reste exposé au phishing en temps réel et au vol du terminal.
9. Le Client ID identifie l'application ; le Client Secret l'authentifie ; PKCE protège l'échange du code, notamment contre l'interception.
10. `localhost` est utilisé par le navigateur ; `authentik-server` est le nom DNS interne utilisable depuis le réseau Docker.
11. Le code d'autorisation est court et échangé côté serveur contre des tokens après authentification et consentement.
12. Un JWT signé permet de détecter une modification, mais son contenu reste lisible sans chiffrement.
13. Le SSO fédère l'authentification ; Grafana conserve ses profils, organisations et permissions propres.
14. Désactiver Authentik bloque les nouvelles connexions, mais une session Grafana déjà établie peut rester valide jusqu'à expiration ou révocation.
