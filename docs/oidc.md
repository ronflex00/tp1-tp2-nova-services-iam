# OIDC Authentik → Grafana

La configuration est manuelle et ne doit commencer qu'après création des utilisateurs/groupes et validation de la MFA.

## Provider

- Name : `nova-grafana-oidc`
- Client type : Confidential
- Authorization flow : `default-provider-authorization-explicit-consent`
- Redirect URI : `http://localhost:3000/login/generic_oauth`
- Matching mode : Strict
- Signing key : certificat auto-signé Authentik ou clé équivalente
- Scope mappings : `openid`, `profile`, `email`, `nova-grafana-groups`

Le Client ID et le Client Secret sont générés dans Authentik, puis placés uniquement dans `.env`. Ne jamais les écrire dans la documentation.

## Application

- Name : `Grafana — Nova Services`
- Slug : `grafana`
- Provider : `nova-grafana-oidc`
- Launch URL : `http://localhost:3000`
- Policy engine mode : ANY
- Bindings : Admin, Dev, RH, Audit

Découverte publique attendue :

```text
http://localhost:9000/application/o/grafana/.well-known/openid-configuration
```

Après création du provider, vérifier la présence de `issuer`, `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint` et `jwks_uri`.

## Configuration Grafana à activer après validation

Ajouter les variables OIDC dans `docker-compose.yml` avec les valeurs `.env`, puis recréer uniquement Grafana. URLs :

- navigateur : `http://localhost:9000/application/o/authorize/`
- conteneur : `http://authentik-server:9000/application/o/token/`
- UserInfo : `http://authentik-server:9000/application/o/userinfo/`

Rôle Grafana :

```text
Admin → Admin
Dev → Editor
RH ou Audit → Viewer
```

Un exemple JWT fictif uniquement :

```json
{
  "iss": "http://localhost:9000/application/o/grafana/",
  "sub": "identifiant-stable-opaque-de-charlie",
  "aud": "identifiant-du-client-grafana",
  "iat": 1800000000,
  "exp": 1800000300,
  "preferred_username": "charlie",
  "email": "charlie@nova-services.test",
  "nova_groups": ["Admin"]
}
```

`iss` identifie l'émetteur, `sub` le sujet stable, `aud` le destinataire, `iat` et `exp` les dates de validité, et `nova_groups` les groupes transmis. Une signature garantit l'intégrité, mais ne chiffre pas le contenu.

