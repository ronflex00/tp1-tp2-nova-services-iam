# Questions TP2

1. L'identité décrit le sujet ; l'authentification vérifie son identité ; l'autorisation décide de ses actions.
2. `role` est une donnée métier. Un droit doit être accordé explicitement par groupe, policy, provider ou application.
3. Un Admin Grafana doit administrer Grafana, pas toute la configuration Authentik ; séparer les périmètres réduit l'impact d'une compromission.
4. Grafana Admin est un rôle d'organisation ; `GrafanaAdmin` est un rôle serveur global plus puissant.
5. Editor est un rôle large au niveau organisation ; il n'est pas limité au dossier Dev sans permissions de dossiers explicites.
6. Retirer les anciens droits évite l'accumulation de privilèges lors d'une mobilité.
7. Enrôler TOTP associe un facteur à un utilisateur ; imposer MFA exige ce facteur dans le parcours de connexion.
8. TOTP réduit le risque lié au mot de passe mais reste exposé au phishing en temps réel et au vol du terminal.
9. Le Client ID identifie l'application ; le Client Secret l'authentifie ; PKCE protège l'échange du code, surtout contre l'interception.
10. `localhost` est l'adresse du navigateur vers Authentik/Grafana ; `authentik-server` est le nom DNS interne utilisable depuis le réseau Docker.
11. Le code d'autorisation est un artefact court échangé côté serveur contre des tokens, après authentification et consentement.
12. Un JWT signé permet de détecter une modification, mais son contenu reste lisible sans chiffrement.
13. Le SSO fédère l'authentification ; Grafana conserve ses propres profils, organisations et permissions.
14. Désactiver Authentik bloque les nouvelles connexions, mais une session Grafana déjà établie peut rester valide jusqu'à expiration ou révocation.

