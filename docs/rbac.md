# RBAC Nova Services

## Matrice Authentik

| Groupe Authentik | Membre initial | Rôle Grafana transmis |
|---|---|---|
| `Admin` | Charlie | `Admin` |
| `Dev` | Bob | `Editor` |
| `RH` | Alice | `Viewer` |
| `Audit` | aucun | `Viewer` |

État initial : Alice est dans `RH`, Bob dans `Dev`, Charlie dans `Admin` et `Audit` est vide. Après le déprovisionnement, Bob n'appartient plus à aucun groupe d'accès ; Alice et Charlie conservent leurs groupes.

`Admin` est un groupe métier Authentik et ne signifie pas Authentik Superuser. Le groupe Admin permet ici le binding de l'application Grafana ; il ne donne pas automatiquement les privilèges d'administration globale d'Authentik.

## Matrice Grafana

| Groupe OIDC `nova_groups` | Rôle Grafana |
|---|---|
| `Admin` | Admin d'organisation |
| `Dev` | Editor |
| `RH` | Viewer |
| `Audit` | Viewer |

Le rôle Admin Grafana est un rôle d'organisation. Il est différent de `GrafanaAdmin`, qui est un rôle serveur global. Le rôle Editor est large au niveau organisation et ne suffit pas, à lui seul, à restreindre automatiquement un utilisateur au dossier Dev.

## Équipes et dossiers

| Équipe | Dossier | Permission directe |
|---|---|---|
| `nova-dev` | `Dev` | Edit |
| `nova-rh` | `RH` | View |

Charlie conserve l'administration des objets Grafana de démonstration.

## Mobilité de Bob

Le scénario prévu retire temporairement Bob de `Dev`, l'ajoute à `Audit`, exige une nouvelle connexion OAuth et vérifie le rôle Viewer. Ce scénario de mobilité n'a pas été exécuté avant le départ final. Le déprovisionnement a ensuite retiré Bob de ses groupes et de `nova-dev`.

## Limite observée

Le test navigateur a montré qu'Alice peut encore ouvrir directement le dashboard Dev malgré l'absence de son appartenance à `nova-dev`. Ce résultat est conservé comme `FAIL` dans `docs/tests.md` : aucune permission n'a été corrigée silencieusement pendant la phase de rendu.

## Property Mapping

Le scope mapping `nova-grafana-groups` expose uniquement les groupes autorisés :

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

L'exemple est documentaire ; aucun token réel n'est enregistré.
