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
| Alice | active | aucun (écart observé le 25/11/2026) | `Viewer` | `nova-rh` |
| Bob | inactive | aucun groupe d'accès | `Editor`, profil non désactivé | absent de `nova-dev` |
| Charlie | active | `Admin` | `Admin` d'organisation | administration conservée |

Le déprovisionnement Authentik de Bob a été exécuté ; le contrôle du 25 novembre confirme son état inactif et l'absence de groupe. La révocation de session Grafana a été demandée lors du départ ; son effet sur une ancienne session n'a pas été observé. La désactivation du profil Grafana a échoué avec HTTP 500. Cela ne démontre pas une limitation générale des profils OAuth externes. Le compte mfa-test est absent.

MFA enregistré au 25 novembre : Charlie a un périphérique TOTP et un dispositif Static ; Bob a un TOTP ; Alice n'a ni TOTP ni Static. Ce contrôle porte uniquement sur les nombres de dispositifs, sans lire leurs secrets. Le groupe RH d'Alice indiqué dans l'état initial n'est plus son état courant.

## Règles de sécurité

- Ne jamais versionner `.env` ou un mot de passe.
- Ne jamais capturer un QR code, un secret TOTP, un recovery code, un token ou un cookie.
- Toute désactivation ou modification de groupe doit être consignée dans la matrice de tests.
