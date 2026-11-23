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
| Identités et attributs | Alice, Bob, Charlie conformes | À confirmer | Capture 01/02 | À TESTER |
| Suspension puis retour de Bob | refus puis autorisation | À confirmer | journal de test | À TESTER |
| Groupes métier | Admin/Dev/RH/Audit | À confirmer | Capture 03/04 | À TESTER |
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

## Cycle de vie Bob

Bob actif → désactivation Authentik → nouvelle connexion refusée → réactivation → nouvelle connexion autorisée. Ce test ne sera PASS qu'après confirmation humaine.

## MFA

Enrôler manuellement dans l'ordre : administrateur Authentik, Charlie, Alice, Bob. Méthode TOTP, puis Static tokens pour la récupération. Configurer Authenticator Validation avec Device classes TOTP/Static, action Not configured = Deny, threshold 0. Ne pas modifier automatiquement les flows via API.

## Scénarios Grafana

Tester en navigation privée : Charlie Admin, Alice Viewer, Bob Editor. Créer le dashboard `Nova Services — Démonstration IAM` avec un panneau texte. Vérifier consultation/modification selon le rôle, changement temporaire de Bob vers Audit, utilisateur Alice sans groupe, dossiers `Dev` et `RH`, puis départ et deprovisioning de Bob.

Le formulaire local ne sera désactivé qu'après validation OIDC complète. Procédure de secours : rétablir temporairement `GF_AUTH_DISABLE_LOGIN_FORM=false` et `GF_AUTH_BASIC_ENABLED=true`, puis recréer uniquement Grafana.

