# Comptes et attributs métier

Les comptes sont créés manuellement dans Authentik → Directory → Users. Ne pas écrire de mot de passe dans ce document.

| Nom | Username | Email | Service | Fonction |
|---|---|---|---|---|
| Alice Martin | `alice` | `alice@nova-services.test` | RH | Responsable RH |
| Bob Dupont | `bob` | `bob@nova-services.test` | Développement | Développeur Backend |
| Charlie Bernard | `charlie` | `charlie@nova-services.test` | IT | Administrateur système |

Paramètres communs : Internal user, Active = oui, Path = `users`.

Attributs à ajouter :

| Utilisateur | `department` | `role` | `clearance_level` |
|---|---|---|---|
| Alice | `RH` | `Manager RH` | `2` |
| Bob | `Development` | `Backend Developer` | `1` |
| Charlie | `IT` | `System Administrator` | `5` |

`role` est un attribut métier. Il ne donne automatiquement ni droit Authentik, ni rôle Grafana, ni privilège système.

Checklist :

- [ ] alice créé
- [ ] bob créé
- [ ] charlie créé
- [ ] mots de passe distincts définis
- [ ] connexion alice vérifiée
- [ ] connexion bob vérifiée
- [ ] connexion charlie vérifiée

