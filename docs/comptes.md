# Comptes et attributs métier

Les mots de passe, secrets MFA et codes de récupération ne sont jamais écrits dans ce document.

## État initial configuré

| Nom | Username | Email | Service | Fonction | Clearance | État |
|---|---|---|---|---|---:|---|
| Alice Martin | `alice` | `alice@nova-services.test` | RH | Manager RH | 2 | active |
| Bob Dupont | `bob` | `bob@nova-services.test` | Development | Backend Developer | 1 | active |
| Charlie Bernard | `charlie` | `charlie@nova-services.test` | IT | System Administrator | 5 | active |

Attributs Authentik vérifiés : `department`, `role` et `clearance_level`. L'attribut métier `role` ne donne à lui seul aucun droit Authentik, Grafana ou système.

## Groupes initiaux

- Alice → `RH`
- Bob → `Dev`
- Charlie → `Admin`
- `Audit` → aucun membre

## État final observé pour cette recette

| Utilisateur | Authentik | Groupe observé | Rôle Grafana observé | Équipe Grafana |
|---|---|---|---|---|
| Alice | active | `RH` | `Viewer` | `nova-rh` |
| Bob | inactive | aucun groupe d'accès | `Editor`, profil non désactivé | absent de `nova-dev` |
| Charlie | active | `Admin` | `Admin` d'organisation | administration conservée |

Le déprovisionnement Authentik de Bob a été exécuté. Sa session Grafana a été révoquée et son équipe `nova-dev` ne le contient plus. La désactivation du profil Grafana externe n'est pas supportée par l'endpoint utilisé et reste `non réalisée`. Le compte `mfa-test` n'a pas été identifié dans l'état contrôlé ; aucune conclusion d'inactivation ne doit être inventée.

## Règles de sécurité

- Ne jamais versionner `.env` ou un mot de passe.
- Ne jamais capturer un QR code, un secret TOTP, un recovery code, un token ou un cookie.
- Toute désactivation ou modification de groupe doit être consignée dans la matrice de tests.
