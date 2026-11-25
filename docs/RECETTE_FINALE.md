# Recette TP1 / TP2 — 25 novembre 2026

## Périmètre

Audit du laboratoire existant, documentation, captures actuelles et contrôles Git. Aucun compte n'a été recréé, Bob n'a pas été réactivé, aucune ACL, configuration OIDC, clé ou volume n'a été changé pour le rendu.

## Contrôles techniques

| Contrôle exécuté | Résultat | Statut |
|---|---|---|
| docker compose config --quiet | valide | PASS |
| docker compose ps | quatre services healthy | PASS |
| scripts/verify.sh | Docker, PostgreSQL, Authentik, worker, Grafana OK | PASS |
| scripts/verify_oidc.sh | découverte, URLs, PKCE, mapping strict, identifiants présents | PASS |
| GET /api/health Grafana | database: ok | PASS |
| Volumes et montages | postgres_data, grafana_data, data/authentik | PASS configuration |
| Persistance avant/après recréation | pas de paire de preuves disponible | PARTIAL |
| Authentification locale Grafana pour consultation | connexion admin et liste des utilisateurs chargées | PASS |
| Connexion OIDC + MFA actuelle | pas rejouée dans cette recette | NOT TESTED |
| Isolation effective des dossiers | anciens contrôles de rendu insuffisants | PARTIAL |
| TOTP incorrect, récupération et réutilisation | aucune validation complète | NOT TESTED |
| Sessions Bob après départ | pas de preuve complète de comportement | NOT TESTED |

Les healthchecks, ports et montages sont contrôlés à partir du Compose et des services existants. Authentik et Grafana utilisent HTTP dans ce laboratoire, avec les ports 9000/3000 publiés sur toutes les interfaces. PostgreSQL n'a pas de port hôte.

## État courant des identités

Mesures effectuées en lecture : requête ciblée sur les objets Authentik via le shell applicatif, sans mot de passe, secret MFA ou code de récupération ; API Grafana avec le compte local existant.

| Compte | Authentik | Groupes Authentik | MFA enregistré | Grafana | Équipe Grafana |
|---|---|---|---|---|---|
| alice | active | aucun | 0 TOTP, 0 Static | Viewer, non désactivée | nova-rh |
| bob | inactive | aucun | 1 TOTP, 0 Static | Editor, non désactivé | absent de nova-dev |
| charlie | active | Admin | 1 TOTP, 1 Static | Admin d'organisation | accès Admin par rôle |
| mfa-test | absent | sans objet | sans objet | non contrôlé | non contrôlé |

Alice n'est donc pas dans RH aujourd'hui, contrairement à l'état initial attendu. Aucun droit n'a été rétabli pendant l'audit.

Le départ de Bob a retiré l'accès Authentik et l'équipe Grafana. L'échec HTTP 500 de désactivation Grafana a été observé lors de la recette précédente ; sa cause n'est pas démontrée. Le rôle Editor restant n'est pas la preuve d'une connexion encore possible.

## Permissions courantes

| Dossier | Permissions renvoyées par l'API | Statut |
|---|---|---|
| Dev | nova-dev : Edit ; charlie : Admin ; aucune entrée Viewer/Editor générale | PASS état ACL |
| RH | nova-rh : View ; charlie : Admin ; aucune entrée Viewer/Editor générale | PASS état ACL |

L'absence d'une entrée générale ne démontre pas le refus d'accès dans une session utilisateur. Le scénario historique n'attendait pas toujours la fin du chargement et ne contrôlait pas l'identité connectée ; ses résultats par compte doivent être relus avec ces réserves.

## Captures

Les [preuves TP1](../captures/tp1/README.md) et [preuves TP2](../captures/tp2/README.md) présentent la sélection publiée. Les images actuelles proviennent de Chromium. Les images historiques des dashboards sont conservées sans reconstituer un ancien état.

Les captures de diagnostic 15-folder-rh.png et 16a-bob-rh-denied.png ont été retirées de la sélection et archivées localement dans un répertoire ignoré. Leur présence dans les commits antérieurs est conservée avec l'historique. Les vues de dashboards ne prouvent pas une sauvegarde, un rôle ou l'identité de la session.

Les nouvelles listes utilisateurs et rôles ont été prises avec le compte local admin ; elles ne prouvent pas les droits d'administration de Charlie dans son navigateur.

## Audit de publication

- Le vrai fichier .env, les données, rapports et sessions sont ignorés.
- Aucun secret local, token GitHub reconnaissable, JWT compact ou clé privée n'a été détecté dans les 69 blobs de l'historique initial.
- Les captures présentes ont été inspectées visuellement : aucun secret visible.
- Les traces Playwright sont désormais désactivées, car elles peuvent conserver des requêtes OAuth ou des saisies.
- Les scans automatiques ont une portée limitée : ils ne garantissent pas l'absence de toute forme de secret inconnue.

## GitHub

Branche conservée : master. Historique conservé. Après l'audit, la publication publique a été demandée explicitement sous ronflex00/tp1-tp2-nova-services-iam.

Dépôt cible : ronflex00/tp1-tp2-nova-services-iam. Les commandes de publication sont :

```bash
git remote add origin https://github.com/ronflex00/tp1-tp2-nova-services-iam.git
git push -u origin master
```

Ne pas forcer le push ; si un historique distant existe, le comparer avant intégration.

## Éléments manquants et statut

Manquent notamment : captures des identités/attributs/groupes/MFA, paire de persistance, mobilité Bob documentée par image, sauvegarde Editor, refus Viewer, tests MFA négatifs/recovery, nouvelle connexion Bob refusée, ancienne session et état final Authentik en image.

La documentation TP1 et TP2, les réponses aux questions, l'architecture, les captures disponibles et les scripts sont présents. Le sujet original complet n'est pas livré dans le dépôt : la correspondance mot à mot des questions ne peut pas être certifiée.

**FINAL STATUS : PARTIAL.** Le dépôt expose honnêtement les preuves disponibles et les scénarios restant à valider.
