# RBAC Nova Services

## Matrice Authentik

| Groupe Authentik | Membre initial | Rôle Grafana transmis |
|---|---|---|
| `Admin` | Charlie | `Admin` |
| `Dev` | Bob | `Editor` |
| `RH` | Alice | `Viewer` |
| `Audit` | aucun | `Viewer` |

État initial prévu : Alice dans RH, Bob dans Dev, Charlie dans Admin et Audit vide. Le contrôle du 25 novembre trouve Alice et Bob sans groupe Authentik, Charlie dans Admin. Alice conserve l'équipe Grafana nova-rh ; Bob est absent de nova-dev. Ces écarts sont consignés sans modifier les droits.

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

Le scénario historique a signalé un accès Alice → Dev, mais son attente de rendu pouvait s'arrêter sur le texte du menu ou une ancienne page. Il ne vérifiait pas non plus l'identité réellement connectée. Le résultat historique FAIL est conservé avec cette réserve, et ne démontre pas la cause.

Au 25 novembre, l'API montre uniquement Charlie → Admin et nova-dev → Edit sur Dev, Charlie → Admin et nova-rh → View sur RH ; aucune entrée générale Viewer/Editor n'est retournée. Aucune permission n'a été changée lors de cet audit.

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
