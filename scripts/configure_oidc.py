#!/usr/bin/env python3
"""Idempotent Authentik -> Grafana OIDC setup for the Nova Services lab.

The API token is read only from AUTHENTIK_API_TOKEN and is never written or
printed. The script follows the live OpenAPI schema exposed by Authentik.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("AUTHENTIK_URL", "http://localhost:9000").rstrip("/")
TOKEN = os.environ.get("AUTHENTIK_API_TOKEN")
MAPPING_NAME = "nova-grafana-groups"
PROVIDER_NAME = "nova-grafana-oidc"
APPLICATION_NAME = "Grafana — Nova Services"
APPLICATION_SLUG = "grafana"
GROUP_NAMES = ("Admin", "Dev", "RH", "Audit")
EXPRESSION = '''allowed_groups = {"Admin", "Dev", "RH", "Audit"}

return {
    "nova_groups": [
        group.name
        for group in request.user.groups.all()
        if group.name in allowed_groups
    ]
}'''


class APIError(RuntimeError):
    def __init__(self, method: str, path: str, status: int, reason: str):
        super().__init__(f"API {method} {path} a échoué (HTTP {status}: {reason})")


class API:
    def __init__(self, token: str):
        self.token = token

    def request(self, method: str, path: str, payload: dict | None = None, query: dict | None = None):
        url = f"{BASE}{path}"
        if query:
            url += "?" + urlencode(query)
        body = None if payload is None else json.dumps(payload).encode()
        req = Request(url, data=body, method=method, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        try:
            with urlopen(req, timeout=20) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except HTTPError as exc:
            # Do not print the response body: it could contain sensitive fields.
            raise APIError(method, path, exc.code, exc.reason) from None
        except URLError as exc:
            raise RuntimeError(f"API inaccessible sur {BASE}: {exc.reason}") from None

    def list_all(self, path: str, query: dict | None = None) -> list[dict]:
        params = {"page_size": 100}
        if query:
            params.update(query)
        result = self.request("GET", path, query=params)
        return result.get("results", [])


def require_token() -> str:
    if not TOKEN:
        print("AUTHENTIK_API_TOKEN manquant", file=sys.stderr)
        raise SystemExit(2)
    return TOKEN


def find_by(items: list[dict], key: str, value: str) -> dict | None:
    return next((item for item in items if item.get(key) == value), None)


def check_state(api: API) -> dict:
    schema = api.request("GET", "/api/v3/schema/", query={"format": "json"})
    version = schema.get("info", {}).get("version", "unknown")
    groups = api.list_all("/api/v3/core/groups/")
    users = api.list_all("/api/v3/core/users/", {"include_groups": "true"})
    flows = api.list_all("/api/v3/flows/instances/")
    keys = api.list_all("/api/v3/crypto/certificatekeypairs/")
    mappings = api.list_all("/api/v3/propertymappings/provider/scope/")
    providers = api.list_all("/api/v3/providers/oauth2/")
    applications = api.list_all("/api/v3/core/applications/", {"superuser_full_list": "true"})
    missing = [name for name in GROUP_NAMES if not find_by(groups, "name", name)]
    if missing:
        raise RuntimeError("Groupe manquant : " + ", ".join(missing))
    users_by_name = {u.get("username"): u for u in users}
    users_by_name.update({u.get("email", "").split("@", 1)[0]: u for u in users if u.get("email")})
    memberships = {}
    for username, group_name in (("alice", "RH"), ("bob", "Dev"), ("charlie", "Admin")):
        user = users_by_name.get(username)
        memberships[username] = {
            "ok": bool(user and any(g.get("name") == group_name for g in user.get("groups_obj") or [])),
            "actual_username": user.get("username") if user else None,
        }
    auth_flows = [f for f in flows if f.get("designation") == "authentication"]
    authorization_flows = [f for f in flows if f.get("designation") == "authorization"]
    invalidation_flows = [f for f in flows if f.get("designation") == "invalidation"]
    auth_flow = find_by(auth_flows, "slug", "default-authentication-flow") or (auth_flows[0] if len(auth_flows) == 1 else None)
    authz_flow = find_by(authorization_flows, "slug", "default-provider-authorization-explicit-consent")
    if not authz_flow and len(authorization_flows) == 1:
        authz_flow = authorization_flows[0]
    invalidation_flow = find_by(invalidation_flows, "slug", "default-provider-invalidation-flow") or (invalidation_flows[0] if len(invalidation_flows) == 1 else None)
    signing_key = next((k for k in keys if k.get("managed") and k.get("private_key_available") and "self" in k.get("name", "").lower()), None)
    if not signing_key:
        signing_key = next((k for k in keys if k.get("private_key_available")), None)
    return {
        "schema_version": version,
        "groups": groups,
        "users": users,
        "memberships": memberships,
        "flows": flows,
        "auth_flow": auth_flow,
        "authz_flow": authz_flow,
        "invalidation_flow": invalidation_flow,
        "signing_key": signing_key,
        "mappings": mappings,
        "providers": providers,
        "applications": applications,
    }


def print_check(state: dict) -> None:
    print(f"Authentik API: OK (schéma {state['schema_version']})")
    print("Groupes: " + ", ".join(GROUP_NAMES))
    for username, result in state["memberships"].items():
        status = "OK" if result["ok"] else "AVERTISSEMENT"
        suffix = "" if result["actual_username"] in (None, username) else " (username existant différent, aucune correction automatique)"
        print(f"Affectation {username}: {status}{suffix}")
    print(f"Flow authentification: {'trouvé' if state['auth_flow'] else 'non résolu'}")
    print(f"Flow autorisation: {'trouvé' if state['authz_flow'] else 'non résolu'}")
    print(f"Flow invalidation: {'trouvé' if state['invalidation_flow'] else 'non résolu'}")
    print(f"Clé de signature: {'trouvée' if state['signing_key'] else 'non résolue'}")
    print(f"Scope mapping {MAPPING_NAME}: {'EXISTING' if find_by(state['mappings'], 'name', MAPPING_NAME) else 'ABSENT'}")
    print(f"Provider {PROVIDER_NAME}: {'EXISTING' if find_by(state['providers'], 'name', PROVIDER_NAME) else 'ABSENT'}")
    print(f"Application {APPLICATION_NAME}: {'EXISTING' if find_by(state['applications'], 'name', APPLICATION_NAME) else 'ABSENT'}")


def update_env(client_id: str, client_secret: str) -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        raise RuntimeError(".env absent")
    if stat.S_IMODE(env_path.stat().st_mode) != 0o600:
        raise RuntimeError(".env doit avoir les permissions 0600")
    lines = env_path.read_text(encoding="utf-8").splitlines()
    replacements = {
        "GRAFANA_OIDC_CLIENT_ID": client_id,
        "GRAFANA_OIDC_CLIENT_SECRET": client_secret,
    }
    found = set()
    output = []
    for line in lines:
        key = line.split("=", 1)[0] if "=" in line else ""
        if key in replacements:
            output.append(f"{key}={replacements[key]}")
            found.add(key)
        else:
            output.append(line)
    for key, value in replacements.items():
        if key not in found:
            output.append(f"{key}={value}")
    fd, temporary = tempfile.mkstemp(prefix=".env.", dir=ROOT, text=True)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write("\n".join(output) + "\n")
        os.replace(temporary, env_path)
        os.chmod(env_path, 0o600)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def apply(api: API, state: dict) -> None:
    auth_flow = state["auth_flow"]
    authz_flow = state["authz_flow"]
    invalidation_flow = state["invalidation_flow"]
    signing_key = state["signing_key"]
    if not all((auth_flow, authz_flow, invalidation_flow, signing_key)):
        raise RuntimeError("Flow ou clé de signature requis introuvable ; aucune modification appliquée")

    mapping = find_by(state["mappings"], "name", MAPPING_NAME)
    if mapping:
        print(f"Mapping {MAPPING_NAME}: EXISTING")
    else:
        mapping = api.request("POST", "/api/v3/propertymappings/provider/scope/", {
            "name": MAPPING_NAME, "scope_name": "nova_groups", "description": "Groupes Nova Services utiles à Grafana", "expression": EXPRESSION,
        })
        print(f"Mapping {MAPPING_NAME}: CREATED")

    provider = find_by(state["providers"], "name", PROVIDER_NAME)
    if provider:
        print(f"Provider {PROVIDER_NAME}: EXISTING")
    else:
        scopes = {"openid", "profile", "email", "nova_groups"}
        property_mappings = [m for m in state["mappings"] if m.get("scope_name") in scopes]
        if not any(m.get("scope_name") == "nova_groups" for m in property_mappings):
            property_mappings.append(mapping)
        missing_scopes = sorted(scopes - {m.get("scope_name") for m in property_mappings})
        if missing_scopes:
            raise RuntimeError("Scope mapping standard manquant : " + ", ".join(missing_scopes))
        provider = api.request("POST", "/api/v3/providers/oauth2/", {
            "name": PROVIDER_NAME,
            "authentication_flow": auth_flow["pk"],
            "authorization_flow": authz_flow["pk"],
            "invalidation_flow": invalidation_flow["pk"],
            "property_mappings": [m["pk"] for m in property_mappings],
            "client_type": "confidential",
            "grant_types": ["authorization_code", "refresh_token"],
            "redirect_uris": [{"matching_mode": "strict", "url": "http://localhost:3000/login/generic_oauth", "redirect_uri_type": "authorization"}],
            "signing_key": signing_key["pk"],
            "include_claims_in_id_token": True,
            "sub_mode": "user_uuid",
            "issuer_mode": "per_provider",
        })
        print(f"Provider {PROVIDER_NAME}: CREATED")

    application = find_by(state["applications"], "slug", APPLICATION_SLUG) or find_by(state["applications"], "name", APPLICATION_NAME)
    if application:
        print(f"Application {APPLICATION_NAME}: EXISTING")
    else:
        application = api.request("POST", "/api/v3/core/applications/", {
            "name": APPLICATION_NAME, "slug": APPLICATION_SLUG, "provider": provider["pk"],
            "meta_launch_url": "http://localhost:3000", "policy_engine_mode": "any",
        })
        print(f"Application {APPLICATION_NAME}: CREATED")

    target = application.get("pbm_uuid") or application.get("pk")
    groups = {g["name"]: g for g in state["groups"]}
    bindings = api.list_all("/api/v3/policies/bindings/", {"target": target})
    for order, name in enumerate(GROUP_NAMES):
        if any((b.get("group_obj") or {}).get("name") == name for b in bindings):
            print(f"Binding {name}: EXISTING")
        else:
            api.request("POST", "/api/v3/policies/bindings/", {"target": target, "group": groups[name]["pk"], "order": order, "enabled": True})
            print(f"Binding {name}: CREATED")

    client_id = provider.get("client_id")
    client_secret = provider.get("client_secret")
    if not client_id or not client_secret:
        raise RuntimeError("Client credentials non récupérables via API ; aucun secret affiché, intervention manuelle requise")
    update_env(client_id, client_secret)
    print(".env: Client ID/Secret mis à jour localement (valeurs non affichées)")


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    api = API(require_token())
    try:
        state = check_state(api)
        if args.check:
            print_check(state)
        else:
            apply(api, state)
        return 0
    except (APIError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

