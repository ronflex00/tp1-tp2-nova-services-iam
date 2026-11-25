# Captures TP2

Les statuts décrivent uniquement les fichiers réellement présents dans ce dossier. Aucune image manquante n'est fabriquée.

| Fichier | Preuve | Statut |
|---|---|---|
| `01-users.png` | Utilisateurs Authentik | MISSING |
| `02-attributes.png` | Attributs métier | MISSING |
| `03-groups.png` | Groupes Admin/Dev/RH/Audit | MISSING |
| `04-memberships.png` | Affectations de groupes | MISSING |
| `05-mfa-devices.png` | Périphériques MFA sans QR code | MISSING |
| `06-mfa-success.png` | MFA réussi | MISSING |
| `07-mfa-denied.png` | MFA refusé | MISSING |
| `08-oidc-provider.png` | Provider sans secret | MISSING |
| `09-grafana-sso.png` | Grafana après connexion OIDC | DONE |
| `10-grafana-users.png` | Liste des trois profils et origine OAuth, compte admin local | DONE |
| `10a-grafana-roles.png` | Rôles d'organisation, compte admin local | DONE |
| `11-dashboard.png` | Dashboard Nova Services | DONE |
| `12-viewer-denied.png` | Alice sans modification | MISSING |
| `13-bob-audit.png` | Bob Viewer après Audit | MISSING |
| `14-folder-dev.png` | Dashboard Dev historique ; compte non identifiable dans l'image | DONE / preuve limitée |
| `15-folder-rh.png` | Diagnostic historique Forbidden ; ne prouve pas la lecture RH | DONE diagnostic / lecture MISSING |
| `16-access-denied.png` | Refus Alice sans groupe | MISSING |
| `16a-bob-rh-denied.png` | Refus RH historique attribué à Bob par le scénario ; identité non visible | DONE / preuve limitée |
| `17-bob-disabled.png` | Bob désactivé | MISSING |
| `18-final-state.png` | État final | MISSING |

Les fichiers DONE ont été contrôlés visuellement et ne montrent pas de mot de passe, QR code, secret TOTP, recovery code, Client Secret, token API, JWT réel, cookie ou `.env`.
