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

## Préparation RBAC Grafana

Préparée par `scripts/prepare_grafana_rbac.py`, de façon idempotente :

| Objet | État | URL/identifiant |
|---|---|---|
| Dashboard principal | créé | `http://localhost:3000/d/nova-services-iam/` |
| Équipe `nova-dev` | créée, Bob membre | équipe Grafana |
| Équipe `nova-rh` | créée, Alice membre | équipe Grafana |
| Dossier `Dev` | créé | `http://localhost:3000/dashboards/f/nova-dev/dev` |
| Dossier `RH` | créé | `http://localhost:3000/dashboards/f/nova-rh/rh` |
| Dashboard Dev | créé | `http://localhost:3000/d/nova-dev-iam/` |
| Dashboard RH | créé | `http://localhost:3000/d/nova-rh-iam/` |

Permissions directes préparées : `nova-dev → Edit`, `nova-rh → View`, Charlie conservé en Admin. Les permissions effectives restent `MANUAL TEST REQUIRED`.

## Scénarios préparés

- `scripts/test_bob_audit.py --apply` puis `--restore` ont été exécutés ; Bob est revenu dans Dev.
- `scripts/test_alice_no_group.py --apply` a été exécuté ; `--restore` reste en attente de la validation manuelle du refus.
- `scripts/deprovision_bob.py --check` est disponible ; `--apply` n'a pas été exécuté.

| Test | Résultat attendu | Résultat observé | Preuve | Statut |
|---|---|---|---|---|
| Charlie Admin Grafana | Admin | rôle API actuel Admin | API Grafana | PASS technique |
| Alice Viewer Grafana | Viewer | rôle API actuel Viewer | API Grafana | PASS technique |
| Bob Editor Grafana | Editor | rôle API actuel Editor | API Grafana | PASS technique |
| Alice dashboard principal | lecture seule | non testé navigateur | `11-dashboard.png` | MANUAL TEST REQUIRED |
| Bob dashboard principal | modification | non testé navigateur | `11-dashboard.png` | MANUAL TEST REQUIRED |
| Bob Dev folder | Edit | non testé navigateur | `14-folder-dev.png` | MANUAL TEST REQUIRED |
| Bob RH folder | refus | non testé navigateur | `15-folder-rh.png` | MANUAL TEST REQUIRED |
| Alice Dev folder | refus | non testé navigateur | `14-folder-dev.png` | MANUAL TEST REQUIRED |
| Alice RH folder | View | non testé navigateur | `15-folder-rh.png` | MANUAL TEST REQUIRED |
| Mobilité Bob Dev → Audit | Viewer après nouvelle connexion OAuth | Viewer confirmé manuellement selon le scénario utilisateur ; capture absente du workspace | `captures/tp2/13-bob-audit.png` attendue | PASS manuel / preuve fichier absente |
| Alice sans RH | refus | scénario appliqué, test navigateur en attente | `16-access-denied.png` | MANUAL TEST REQUIRED |
| Bob deprovisioning | accès retirés | non démarré | `17-bob-disabled.png` | NOT STARTED |

## État après mobilité Bob

Bob a été restauré dans `Dev` et retiré de `Audit`. Son rôle Grafana doit redevenir Editor après une nouvelle connexion OAuth ; le rôle API observé avant cette reconnexion peut encore être Viewer. Aucun rôle Grafana n'a été modifié directement.

## État du test Alice sans groupe

Alice a été retirée temporairement de `RH` et n'appartient plus à aucun groupe autorisé par l'application Grafana. Le refus doit être vérifié dans une nouvelle fenêtre privée avant restauration. Le script `test_alice_no_group.py --restore` n'a pas encore été exécuté.

## Cycle de vie Bob

Bob actif → désactivation Authentik → nouvelle connexion refusée → réactivation → nouvelle connexion autorisée. Ce test ne sera PASS qu'après confirmation humaine.

## MFA

Enrôler manuellement dans l'ordre : administrateur Authentik, Charlie, Alice, Bob. Méthode TOTP, puis Static tokens pour la récupération. Configurer Authenticator Validation avec Device classes TOTP/Static, action Not configured = Deny, threshold 0. Ne pas modifier automatiquement les flows via API.

## Scénarios Grafana

Tester en navigation privée : Charlie Admin, Alice Viewer, Bob Editor. Créer le dashboard `Nova Services — Démonstration IAM` avec un panneau texte. Vérifier consultation/modification selon le rôle, changement temporaire de Bob vers Audit, utilisateur Alice sans groupe, dossiers `Dev` et `RH`, puis départ et deprovisioning de Bob.

Le formulaire local ne sera désactivé qu'après validation OIDC complète. Procédure de secours : rétablir temporairement `GF_AUTH_DISABLE_LOGIN_FORM=false` et `GF_AUTH_BASIC_ENABLED=true`, puis recréer uniquement Grafana.

