# Tests TP2

## Règle de statut

`PASS` est réservé à un résultat réellement observé. `PARTIAL` indique qu'une partie de la preuve est disponible mais qu'une action, une capture ou une vérification complémentaire manque. `NOT TESTED` indique qu'aucune exécution fiable n'a été réalisée.

## Matrice de validation réelle

| Test | Résultat attendu | Résultat observé | Preuve | Statut |
|---|---|---|---|---|
| Identités et attributs | Alice, Bob et Charlie conformes | Vérifiés précédemment par API | Pas de capture 01/02 | PARTIAL |
| Suspension/réactivation Bob | refus puis autorisation | Scénario non exécuté dans la recette finale | aucune | NOT TESTED |
| Groupes métier | Admin/Dev/RH/Audit | Alice RH, Bob Dev, Charlie Admin, Audit vide | Pas de capture 03/04 | PARTIAL |
| MFA obligatoire | facteur exigé | MFA saisi manuellement pour les trois connexions navigateur | aucune capture MFA | PARTIAL |
| Charlie TOTP valide | connexion acceptée | Connexion Charlie réussie avec MFA | `09-grafana-sso.png` | PASS manuel |
| Charlie TOTP incorrect | connexion refusée | Non exécuté | aucune | NOT TESTED |
| Recovery code première utilisation | accepté | Non exécuté | aucune | NOT TESTED |
| Recovery code seconde utilisation | refusé | Non exécuté | aucune | NOT TESTED |
| Alice Viewer | rôle Viewer | API Grafana : Viewer ; dashboard visible | `11-dashboard.png` | PARTIAL |
| Bob Editor | rôle Editor | API Grafana : Editor ; dashboard visible | `11-dashboard.png` | PARTIAL |
| Charlie Admin | Admin d'organisation | API Grafana : Admin | pas de capture 10 | PARTIAL |
| Alice dashboard lecture seule | lecture sans modification | Modification non tentée | `11-dashboard.png` | NOT TESTED |
| Bob dashboard modification | sauvegarde autorisée puis restauration | Modification non tentée | `11-dashboard.png` | NOT TESTED |
| Bob dossier Dev | accès et édition | Dashboard visible, bouton Edit visible | `14-folder-dev.png` | PARTIAL |
| Bob refus dossier RH | accès refusé | Grafana affiche Forbidden | `16a-bob-rh-denied.png` | PASS |
| Alice refus dossier Dev | accès refusé | Dashboard Dev encore accessible | aucune | FAIL |
| Alice lecture dossier RH | lecture autorisée | Dashboard RH visible | `15-folder-rh.png` | PARTIAL |
| Bob Dev → Audit → Viewer | rôle Viewer après reconnexion | Non exécuté : jeton API absent de l'environnement | aucune | NOT TESTED |
| Alice sans groupe autorisé | accès refusé | Non exécuté | aucune | NOT TESTED |
| Déprovisioning Bob | compte et accès retirés | Non exécuté | aucune | NOT TESTED |
| Nouvelle connexion Bob après départ | refusée | Non exécuté | aucune | NOT TESTED |
| Ancienne session Bob après départ | comportement documenté | Non exécuté | aucune | NOT TESTED |

## Captures navigateur réalisées

- `09-grafana-sso.png` : Grafana après authentification OIDC réussie.
- `11-dashboard.png` : dashboard principal Nova Services.
- `14-folder-dev.png` : dashboard Dev accessible à Bob avec l'action Edit visible.
- `15-folder-rh.png` : dashboard RH accessible à Alice.
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
