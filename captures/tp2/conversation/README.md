# Captures utiles récupérées de la conversation

Ces captures ont été réellement transmises dans la conversation et sont classées comme **preuves historiques** du TP2. Elles ne sont pas nécessairement l’état final du laboratoire. Elles ont été recadrées pour retirer les onglets du navigateur / la conversation adjacente lorsque pertinent ; les informations de preuve n’ont pas été modifiées.

Aucune capture exploitable du TP1 (conteneurs, persistance, Grafana initial) n’a été retrouvée parmi les images jointes disponibles. Les captures AWS du TP3 ont été exclues.

| Fichier | Description / limite |
|---|---|
| [01-users-authentik.png](01-users-authentik.png) | INTÉGRÉE — comptes actifs avant le départ de Bob ; usernames encore longs. |
| [02-attributs-charlie.png](02-attributs-charlie.png) | INTÉGRÉE — attributs role, department et clearance_level de Charlie uniquement ; capture historique. |
| [03-groupes-crees.png](03-groupes-crees.png) | INTÉGRÉE — groupes à leur création, effectifs à zéro ; Rh avec casse intermédiaire. |
| [04-appartenances-historique.png](04-appartenances-historique.png) | INTÉGRÉE — effectifs 1/0/1/1 pour Admin/Audit/DEV/RH ; aucun nom de membre visible. |
| [05-mfa-akadmin-totp.png](05-mfa-akadmin-totp.png) | INTÉGRÉE — TOTP enregistré ; attribution akadmin selon le contexte, nom non visible ; aucune dernière utilisation, QR ou seed. |
| `06-mfa-charlie-totp.png` | LOCALE / EXCLUE — avatar BD, attribution à Charlie non démontrée ; aucune preuve de connexion MFA. |
| `09-sso-consentement-authentik.png` | LOCALE / EXCLUE — consentement avec conversation adjacente ; pas publiée pour limiter les informations hors sujet. |
| `10a-sso-charlie-grafana.png` | LOCALE / EXCLUE — conversation adjacente et vue de profils moins complète que 10-grafana-users.png existante. |
| `10-grafana-roles-oidc.png` | LOCALE / REDONDANTE — rôles tronqués ; la capture existante 10a-grafana-roles.png est plus lisible. |
| `11-dashboard-iam.png` | LOCALE / REDONDANTE — même panneau Text que 11-dashboard.png existante. |
| [14-dossier-dev-bob.png](14-dossier-dev-bob.png) | INTÉGRÉE — identités admin/Bob visibles ; RH absent de la liste Bob, sans preuve de refus sur URL directe. |
| [13-bob-viewer-apres-mobilite.png](13-bob-viewer-apres-mobilite.png) | INTÉGRÉE — bob Viewer et synchronisation Generic OAuth visibles ; groupe Audit, refus d'édition et restauration non visibles. |

## Utilisation dans le dépôt

Sélection du 26 novembre 2026 : sept images intégrées sans écraser les captures existantes, cinq laissées localement et ignorées par Git. Aucun doublon binaire SHA-256 n'a été trouvé entre les 12 images et les cinq PNG TP2 existants. Les doublons écartés sont fonctionnels : une autre image illustre déjà la même information plus clairement.

Les sept preuves sont légendées dans le [compte rendu](../../../docs/compte-rendu-tp2.md) et répertoriées dans la [matrice des tests](../../../docs/tests.md). La liste des utilisateurs et Bob Viewer sont aussi affichés dans le [README global](../../../README.md). Aucun scénario complet ne reçoit PASS sur la seule base de ces images.

## Confidentialité

Inspection visuelle des 12 images : aucun secret TOTP, QR d'enrôlement, recovery code, token API, cookie, JWT ou mot de passe lisible détecté. La fiche Bob contient un champ mot de passe masqué, des dates de session et une adresse privée Docker, sans identifiant de session. Les noms et adresses nova-services.test correspondent aux identités du TP ; aucune adresse personnelle externe n'est visible dans les images sélectionnées. Les deux vues avec conversation adjacente ne sont pas incluses dans le commit.

Les originaux écartés restent sur le poste. Leurs noms sont volontairement présentés sans liens Markdown, car ils ne seront pas disponibles sur GitHub.

À compléter par des captures préexistantes ou nouvelles : TP1 Docker/persistance, refus Alice URL Dev, refus Bob URL RH, résultat Alice sans groupe, déprovisionnement final Bob. Ces preuves ne sont pas toutes présentes dans les fichiers de cette conversation.
