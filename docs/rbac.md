# RBAC Nova Services

## Groupes et affectations

| Groupe | Utilisateur initial | Rôle Grafana cible |
|---|---|---|
| `Admin` | Charlie | Admin |
| `Dev` | Bob | Editor |
| `RH` | Alice | Viewer |
| `Audit` | aucun | Viewer |

Créer les groupes dans Authentik → Directory → Groups. `Admin` ne doit pas être Authentik Superuser : Admin Grafana et Superuser Authentik sont deux périmètres différents.

Affectations initiales : `alice → RH`, `bob → Dev`, `charlie → Admin`.

## Mobilité de Bob

Pour le test, retirer temporairement Bob de `Dev`, l'ajouter à `Audit`, effectuer une nouvelle connexion OAuth et vérifier le rôle Viewer. Puis remettre Bob dans `Dev` et retirer `Audit`. Conserver simultanément plusieurs groupes peut augmenter les privilèges effectifs.

## Mapping des groupes

Property Mapping Authentik, type OAuth2/OpenID Scope Mapping :

- Name : `nova-grafana-groups`
- Scope name : `nova_groups`

```python
allowed_groups = {"Admin", "Dev", "RH", "Audit"}

return {
    "nova_groups": [
        group.name
        for group in request.user.groups.all()
        if group.name in allowed_groups
    ]
}
```

Exemple fictif : `{"nova_groups": ["Admin"]}`. Aucun vrai token n'est enregistré.

