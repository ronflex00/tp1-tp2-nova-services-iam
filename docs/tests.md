# Tests TP2

## État laboratoire observé

Le 23 novembre 2026, avant configuration TP2 :

- `docker compose config --services` : PASS, quatre services attendus
- `docker compose ps` : PASS, quatre services healthy
- endpoint Authentik default flow : PASS, HTTP 200
- API Grafana : PASS, `database: ok`
- `./scripts/verify.sh` : PASS

## Matrice de validation

| Test | Résultat attendu | Résultat observé | Preuve | Statut |
|---|---|---|---|---|
| Identités et attributs | Alice, Bob, Charlie conformes | Vérifiés par API : usernames, noms et attributs conformes | Capture 01/02 à prendre | PASS technique / capture à faire |
| Suspension puis retour de Bob | refus puis autorisation | À confirmer | journal de test | À TESTER |
| Groupes métier | Admin/Dev/RH/Audit | Vérifiés par API : affectations conformes, Audit vide | Capture 03/04 à prendre | PASS technique / capture à faire |
| Compte sans facteur après MFA obligatoire | refus | À confirmer | Capture 07 | À TESTER |
| Charlie + TOTP valide | PASS | À confirmer | Capture 06 | À TESTER |
| Charlie + TOTP incorrect | refus | À confirmer | Capture 07 | À TESTER |
| Code récupération première utilisation | accepté | À confirmer | procédure | À TESTER |
| Même code seconde utilisation | refus | À confirmer | procédure | À TESTER |
| Alice Viewer / Bob Editor / Charlie Admin | rôles corrects | À confirmer | Capture 10 | À TESTER |
| Alice sans groupe | accès refusé | À confirmer | Capture 16 | À TESTER |
| Bob Audit → Viewer | modification refusée | À confirmer | Capture 13 | À TESTER |
| Dossiers RH et Dev | permissions correctes | À confirmer | Capture 14/15 | À TESTER |
| Bob désactivé dans Authentik | nouvelle connexion refusée | À confirmer | Capture 17 | À TESTER |
| Deprovisioning complet | sessions et accès retirés | À confirmer | Capture 18 | À TESTER |

## Validation technique OIDC

Après configuration, `scripts/verify_oidc.sh` est PASS pour :

- provider/application accessibles par la découverte OIDC ;
- issuer, authorization endpoint, token endpoint, UserInfo et JWKS ;
- Grafana healthy ;
- Generic OAuth activé, PKCE actif et URLs front/back-channel correctes ;
- présence des identifiants OIDC sans afficher leurs valeurs.

Cela ne remplace pas les connexions humaines et le contrôle des rôles.

## Diagnostic SSO Alice/Bob

Les logs observés montrent :

- Authentik authentifie et autorise Alice et Bob avec les scopes `openid profile email nova_groups` ;
- les claims prévisualisées contiennent respectivement `nova_groups: ["RH"]` et `nova_groups: ["Dev"]` ;
- le provider est confidentiel, son redirect URI est strict et correct ;
- l'application contient les bindings Admin, Dev, RH et Audit ;
- Grafana enregistre `auth.oauth.state.missing` lors de retours OAuth relancés depuis une session qui ne possède plus le cookie d'état.

Cause observée : le callback OAuth n'est pas repris dans la même session navigateur que celle qui a lancé `/login/generic_oauth` (cookie d'état absent, session périmée ou URL de callback rejouée). Aucun défaut de mapping de rôle n'a été trouvé.

Correction opérationnelle : ouvrir une fenêtre privée, utiliser `http://localhost:3000` puis le bouton `Authentik - Nova Services`, conserver `localhost` dans les deux URLs et ne pas ouvrir directement une ancienne URL `/login/generic_oauth`. Les cookies de `localhost:3000` peuvent être supprimés avant un nouvel essai. Cette correction n'a nécessité aucune modification Authentik, aucun changement de rôle et aucun redémarrage de service.

État des tests utilisateurs : Alice → Viewer et Bob → Editor restent à valider dans un navigateur propre.

## Cycle de vie Bob

Bob actif → désactivation Authentik → nouvelle connexion refusée → réactivation → nouvelle connexion autorisée. Ce test ne sera PASS qu'après confirmation humaine.

## MFA

Enrôler manuellement dans l'ordre : administrateur Authentik, Charlie, Alice, Bob. Méthode TOTP, puis Static tokens pour la récupération. Configurer Authenticator Validation avec Device classes TOTP/Static, action Not configured = Deny, threshold 0. Ne pas modifier automatiquement les flows via API.

## Scénarios Grafana

Tester en navigation privée : Charlie Admin, Alice Viewer, Bob Editor. Créer le dashboard `Nova Services — Démonstration IAM` avec un panneau texte. Vérifier consultation/modification selon le rôle, changement temporaire de Bob vers Audit, utilisateur Alice sans groupe, dossiers `Dev` et `RH`, puis départ et deprovisioning de Bob.

Le formulaire local ne sera désactivé qu'après validation OIDC complète. Procédure de secours : rétablir temporairement `GF_AUTH_DISABLE_LOGIN_FORM=false` et `GF_AUTH_BASIC_ENABLED=true`, puis recréer uniquement Grafana.

