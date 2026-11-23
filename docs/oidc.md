# OIDC Authentik → Grafana

## Rôles

- Authentik est l'Identity Provider.
- Grafana est l'application cliente OIDC.

## Flux

```text
Navigateur
  → Grafana
  → Authentik
  → login + MFA
  → authorization code
  → Grafana
  → token endpoint
  → userinfo
  → claim nova_groups
  → rôle Grafana
```

Front channel navigateur : `http://localhost:9000`.

Back channel depuis Grafana : `http://authentik-server:9000`.

## Provider Authentik

- Nom : `nova-grafana-oidc`
- Type client : Confidential
- Redirect URI stricte : `http://localhost:3000/login/generic_oauth`
- Scope mapping : `openid`, `profile`, `email`, `nova-grafana-groups`
- Claim de groupes : `nova_groups`
- Application : `Grafana — Nova Services`
- Bindings : `Admin`, `Dev`, `RH`, `Audit`

Le Client ID et le Client Secret sont conservés uniquement dans `.env`. Aucune valeur réelle n'est documentée.

## Découverte

```text
http://localhost:9000/application/o/grafana/.well-known/openid-configuration
```

La découverte doit exposer `issuer`, `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint` et `jwks_uri`.

## Mapping

```text
Admin → Admin
Dev   → Editor
RH    → Viewer
Audit → Viewer
```

PKCE est activé. La validation technique de la découverte et de la configuration Grafana est réalisée par `scripts/verify_oidc.sh`; elle ne remplace pas les connexions humaines.
