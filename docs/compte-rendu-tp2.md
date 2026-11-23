# TP2 — Gestion des identités, RBAC, MFA et SSO

## 1. Contexte

Nova Services poursuit le laboratoire TP1 PostgreSQL, Authentik et Grafana. Gitea n'est pas retenu.

## 2. Architecture

Authentik reste le fournisseur d'identité. Grafana délègue l'authentification via OIDC ; PostgreSQL reste interne à Authentik.

## 3. Gestion des identités

Alice, Bob et Charlie sont à créer manuellement selon `docs/comptes.md`.

## 4. Attributs métier

Les attributs `department`, `role` et `clearance_level` sont documentés sans secret.

## 5. Cycle de vie

Le scénario de suspension/réactivation de Bob est défini dans `docs/tests.md`.

## 6. RBAC

Les groupes Admin, Dev, RH et Audit, leurs membres et la mobilité de Bob sont définis dans `docs/rbac.md`.

## 7. MFA

Enrôlement TOTP manuel et validation obligatoire à confirmer humainement.

## 8. Procédure de récupération

Voir `docs/recovery.md`.

## 9. OIDC

Provider `nova-grafana-oidc`, scope mapping `nova-grafana-groups` et application Grafana sont décrits dans `docs/oidc.md`.

## 10. Intégration Grafana

Le provider `nova-grafana-oidc`, l'application `Grafana — Nova Services` et les bindings Admin/Dev/RH/Audit ont été créés via l'API Authentik. Grafana utilise désormais Generic OAuth avec PKCE, la découverte d'identifiants et les URLs front-channel/back-channel documentées.

## 11. Mapping des rôles

Admin → Admin, Dev → Editor, RH/Audit → Viewer.

## 12. Permissions de dossiers

À tester avec les dossiers Dev et RH, leurs équipes et leurs permissions dédiées.

## 13. Tests

Les tests TP1 et les tests techniques OIDC sont PASS. Les tests humains TP2 restent `À TESTER` jusqu'à preuve par captures ou validation explicite.

## 14. Départ de Bob

Désactivation, révocation des sessions, retrait des groupes et désactivation Grafana à réaliser en dernier.

## 15. Sécurité

Aucun secret OIDC, mot de passe, QR code MFA, recovery code ou token réel ne doit être stocké dans Git.

## 16. Conclusion

Le laboratoire TP1 est opérationnel et le plan TP2 est préparé sans inventer de validations manuelles.

