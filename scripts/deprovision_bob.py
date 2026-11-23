#!/usr/bin/env python3
"""Explicit Bob deprovisioning tool. --apply is intentionally never run automatically."""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from authentik_api import AuthentikAPI

GRAFANA = os.environ.get("GRAFANA_URL", "http://localhost:3000").rstrip("/")


def grafana_request(method: str, path: str, password: str, payload=None):
    token = base64.b64encode(f"admin:{password}".encode()).decode()
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(GRAFANA + path, data=data, method=method, headers={"Authorization": f"Basic {token}", "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urlopen(req, timeout=20) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        raise RuntimeError(f"Grafana API {method} {path}: HTTP {exc.code}") from None
    except URLError as exc:
        raise RuntimeError(f"Grafana inaccessible sur {GRAFANA}: {exc.reason}") from None


def load_password():
    values = {}
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    for line in (root / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values.get("GRAFANA_ADMIN_PASSWORD")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        api = AuthentikAPI()
        bob = api.user("bob")
        if not bob:
            raise RuntimeError("Utilisateur Bob introuvable")
        groups = [g.get("name") for g in bob.get("groups_obj") or []]
        print(f"Bob actif Authentik: {'oui' if bob.get('is_active') else 'non'}")
        print("Groupes Bob: " + (", ".join(groups) if groups else "aucun"))
        password = load_password()
        if not password:
            raise RuntimeError("GRAFANA_ADMIN_PASSWORD manquant")
        users = grafana_request("GET", "/api/org/users", password)
        grafana_bob = next((u for u in users if u.get("login") == "bob"), None)
        if grafana_bob:
            print(f"Bob Grafana: role={grafana_bob.get('role')}, disabled={'oui' if grafana_bob.get('isDisabled') else 'non'}")
        else:
            print("Bob Grafana: profil introuvable")
        if args.check:
            return 0
        # Explicit apply only: no password, MFA, user deletion or volume changes.
        api.request("PATCH", f"/api/v3/core/users/{bob['pk']}/", {"is_active": False})
        for name in ("Dev", "Audit"):
            group_obj = api.group(name)
            if group_obj and api.has_membership(bob, name):
                api.remove_user(group_obj, bob)
        api.request("DELETE", "/api/v3/core/authenticated_sessions/bulk_delete/", query={"user_pks": bob["pk"]})
        if grafana_bob:
            gid = grafana_bob["id"]
            grafana_request("POST", f"/api/admin/users/{gid}/logout", password)
            grafana_request("PUT", f"/api/users/{gid}", password, {"isDisabled": True})
            teams = grafana_request("GET", "/api/teams/search?perpage=100", password).get("teams", [])
            for team in teams:
                if team.get("name") == "nova-dev":
                    grafana_request("DELETE", f"/api/teams/{team['id']}/members/{gid}", password)
        print("Deprovisioning Bob appliqué; vérifier les sessions et permissions manuellement.")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
