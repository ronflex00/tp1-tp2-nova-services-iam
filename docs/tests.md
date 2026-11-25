# Tests TP2

## Règle de statut

`PASS` est réservé à un résultat réellement observé. `PARTIAL` indique qu'une partie de la preuve est disponible mais qu'une action, une capture ou une vérification complémentaire manque. `NOT TESTED` indique qu'aucune exécution fiable n'a été réalisée.

## Matrice de validation réelle

| Test | Résultat attendu | Résultat observé | Preuve | Statut |
|---|---|---|---|---|
| Identités et attributs | Alice, Bob et Charlie conformes | Vérifiés précédemment par API | Pas de capture 01/02 | PARTIAL |
| Suspension/réactivation Bob | refus puis autorisation | Suspension exécutée ; réactivation non exécutée | aucune | PARTIAL |
| Groupes métier | Admin/Dev/RH/Audit | Alice RH, Charlie Admin, Bob sans groupe après départ, Audit vide | Pas de capture 03/04 | PARTIAL |
| MFA obligatoire | facteur exigé | MFA saisi manuellement pour les trois connexions navigateur | aucune capture MFA | PARTIAL |
| Charlie TOTP valide | connexion acceptée | Connexion Charlie réussie avec MFA | `09-grafana-sso.png` | PASS manuel |
| Charlie TOTP incorrect | connexion refusée | Non exécuté | aucune | NOT TESTED |
| Recovery code première utilisation | accepté | Non exécuté | aucune | NOT TESTED |
| Recovery code seconde utilisation | refusé | Non exécuté | aucune | NOT TESTED |
| Alice Viewer | rôle Viewer | API et vue des utilisateurs d'organisation : Viewer | 10a-grafana-roles.png | PASS rôle |
| Bob Editor | rôle Editor | API et vue des utilisateurs d'organisation : Editor, sans preuve de sauvegarde | 10a-grafana-roles.png | PASS rôle |
| Charlie Admin | Admin d'organisation | API et vue des utilisateurs d'organisation : Admin | 10a-grafana-roles.png | PASS rôle |
| Alice dashboard lecture seule | lecture sans modification | Modification non tentée | `11-dashboard.png` | NOT TESTED |
| Bob dashboard modification | sauvegarde autorisée puis restauration | Modification non tentée | `11-dashboard.png` | NOT TESTED |
| Bob dossier Dev | accès et édition | Dashboard visible, bouton Edit visible | `14-folder-dev.png` | PARTIAL |
| Bob refus dossier RH | accès refusé | Grafana affiche Forbidden | `16a-bob-rh-denied.png` | PASS |
| Alice refus dossier Dev | accès refusé | Dashboard Dev encore accessible | aucune | FAIL |
| Alice lecture dossier RH | lecture autorisée | L'image actuelle affiche Forbidden ; identité de session non contrôlée | `15-folder-rh.png` | PARTIAL |
| Bob Dev → Audit → Viewer | rôle Viewer après reconnexion | Non exécuté avant le départ final | aucune | NOT TESTED |
| Alice sans groupe autorisé | accès refusé | Non exécuté | aucune | NOT TESTED |
| Déprovisioning Bob | compte et accès retirés | Authentik inactif, groupes retirés, session Grafana révoquée, équipe retirée ; profil Grafana externe non désactivé | aucune | PARTIAL |
| Nouvelle connexion Bob après départ | refusée | Fenêtre fermée avant observation du refus | `17-bob-disabled.png` absent | NOT TESTED |
| Ancienne session Bob après départ | comportement documenté | Session conservée avant révocation, résultat du refresh non récupéré | aucune | NOT TESTED |

## Réserves et contrôle du 25 novembre 2026

La matrice ci-dessus retrace la recette précédente ; les observations suivantes précisent sa portée :

- Alice est active, sans groupe Authentik et sans périphérique TOTP/Static ; son profil Grafana est Viewer dans nova-rh. L'ancienne mention Alice RH est un état initial, pas l'état final mesuré.
- Bob est inactif Authentik, sans groupe et absent de nova-dev. Son profil Grafana reste Editor, non désactivé. Charlie reste actif, groupe Admin, rôle Admin d'organisation.
- Charlie possède un TOTP et un dispositif Static ; Bob possède un TOTP. Leur présence ne prouve ni le refus d'un code incorrect ni l'usage unique des codes de récupération.
- La capture 15-folder-rh.png montre Forbidden. La lecture RH par Alice est donc PARTIAL : l'image actuelle ne la prouve pas et le scénario ne vérifiait pas l'identité connectée.
- Les images 11 et 14 montrent les dashboards et un bouton Edit, pas une sauvegarde réussie ni l'identité connectée. Le test Bob Editor reste PARTIAL.
- Le refus RH de 16a est visible, mais son attribution à Bob repose sur le déroulé historique, pas sur une identité visible dans l'image.
- Les attentes Playwright historiques pouvaient accepter un menu ou un ancien rendu ; les échecs Alice Dev et Charlie Users doivent être rejoués avec contrôle de l'identité et de la réponse API avant d'en déduire une cause.
- L'erreur HTTP 500 de désactivation Grafana est observée ; aucune incompatibilité générale des comptes OAuth n'est démontrée.

Le rendu n'a relancé aucune mutation ou connexion Bob. Voir [RECETTE_FINALE.md](RECETTE_FINALE.md) pour la synthèse des mesures actuelles.

## Captures navigateur réalisées

- `09-grafana-sso.png` : Grafana après authentification OIDC réussie.
- 10-grafana-users.png et 10a-grafana-roles.png : profils OAuth et rôles actuels, consultés avec admin local le 25 novembre.
- `11-dashboard.png` : dashboard principal Nova Services.
- `14-folder-dev.png` : dashboard Dev accessible à Bob avec l'action Edit visible.
- `15-folder-rh.png` : diagnostic Forbidden ; ne prouve pas un accès RH autorisé.
- `16a-bob-rh-denied.png` : refus d'accès de Bob au dashboard RH.

Les captures ont été inspectées et ne contiennent ni secret, ni QR code, ni token, ni cookie visible.

## Validation technique OIDC

Les vérifications techniques suivantes sont exécutées avant le commit final :

```bash
docker compose config --quiet
docker compose ps
bash scripts/verify.sh
bash scripts/verify_oidc.sh
curl -fsS http://localhost:3000/api/health
curl -fsS http://localhost:9000/application/o/grafana/.well-known/openid-configuration | python3 -m json.tool
```

Ces contrôles ne remplacent pas les tests humains MFA/RBAC.
