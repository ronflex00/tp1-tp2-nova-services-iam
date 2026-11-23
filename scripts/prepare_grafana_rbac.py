#!/usr/bin/env python3
"""Idempotently prepare Nova Services Grafana teams, folders and dashboards."""
from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("GRAFANA_URL", "http://localhost:3000").rstrip("/")


def load_env() -> dict[str, str]:
    values = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value
    return values


class Grafana:
    def __init__(self, password: str):
        token = base64.b64encode(f"admin:{password}".encode()).decode()
        self.headers = {"Authorization": f"Basic {token}", "Accept": "application/json", "Content-Type": "application/json"}

    def request(self, method: str, path: str, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = Request(BASE + path, data=data, method=method, headers=self.headers)
        try:
            with urlopen(req, timeout=20) as response:
                raw = response.read()
                return response.status, (json.loads(raw) if raw else {})
        except HTTPError as exc:
            body = exc.read().decode(errors="replace")
            # Keep error output short and never include request credentials.
            raise RuntimeError(f"Grafana API {method} {path}: HTTP {exc.code} {body[:240]}") from None
        except URLError as exc:
            raise RuntimeError(f"Grafana inaccessible sur {BASE}: {exc.reason}") from None


def find_dashboard(api: Grafana, uid: str):
    try:
        status, data = api.request("GET", f"/api/dashboards/uid/{uid}")
        return data.get("dashboard")
    except RuntimeError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def find_folder(api: Grafana, uid: str):
    try:
        _, data = api.request("GET", f"/api/folders/{uid}")
        return data
    except RuntimeError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def ensure_team(api: Grafana, name: str) -> dict:
    _, data = api.request("GET", "/api/teams/search?perpage=100")
    team = next((x for x in data.get("teams", []) if x.get("name") == name), None)
    if team:
        print(f"Team {name}: EXISTING")
        return team
    api.request("POST", "/api/teams", {"name": name})
    _, refreshed = api.request("GET", "/api/teams/search?perpage=100")
    created = next((x for x in refreshed.get("teams", []) if x.get("name") == name), None)
    if not created:
        raise RuntimeError(f"Équipe créée mais introuvable après création : {name}")
    print(f"Team {name}: CREATED")
    return created


def ensure_member(api: Grafana, team_id: int, team_name: str, user_id: int, login: str) -> None:
    _, data = api.request("GET", f"/api/teams/{team_id}/members")
    if any(m.get("userId") == user_id for m in data):
        print(f"Membership {login}->{team_name}: EXISTING")
        return
    api.request("POST", f"/api/teams/{team_id}/members", {"userId": user_id})
    print(f"Membership {login}->{team_name}: CREATED")


def ensure_folder(api: Grafana, uid: str, title: str) -> dict:
    folder = find_folder(api, uid)
    if folder:
        print(f"Folder {title}: EXISTING")
        return folder
    _, folder = api.request("POST", "/api/folders", {"uid": uid, "title": title})
    print(f"Folder {title}: CREATED")
    return folder


def ensure_dashboard(api: Grafana, uid: str, title: str, content: str, folder_uid: str | None = None) -> dict:
    existing = find_dashboard(api, uid)
    if existing:
        print(f"Dashboard {title}: EXISTING uid={uid}")
        return existing
    dashboard = {
        "uid": uid,
        "title": title,
        "tags": ["nova-services", "iam"],
        "timezone": "browser",
        "schemaVersion": 39,
        "version": 1,
        "panels": [{
            "id": 1, "type": "text", "title": "Nova Services IAM",
            "gridPos": {"h": 5, "w": 24, "x": 0, "y": 0},
            "options": {"mode": "markdown", "content": content},
        }],
    }
    payload = {"dashboard": dashboard, "folderUid": folder_uid or "", "overwrite": False}
    _, result = api.request("POST", "/api/dashboards/db", payload)
    print(f"Dashboard {title}: CREATED uid={result.get('uid', uid)}")
    return dashboard


def set_folder_permissions(api: Grafana, folder_uid: str, team_id: int, team_name: str, permission: int, charlie_id: int) -> None:
    # PUT replaces direct permissions. Keep Charlie's explicit admin access and
    # only the intended team access; organization admins retain administration.
    payload = {"items": [
        {"teamId": team_id, "permission": permission},
        {"userId": charlie_id, "permission": 4},
    ]}
    # Grafana 13.3.1 exposes this update as POST (PUT returns 404).
    api.request("POST", f"/api/folders/{folder_uid}/permissions", payload)
    level = {1: "View", 2: "Edit", 4: "Admin"}[permission]
    print(f"Permissions {folder_uid}: {team_name}={level}, Charlie=Admin")


def main() -> int:
    try:
        env = load_env()
        password = env.get("GRAFANA_ADMIN_PASSWORD")
        if not password:
            print("GRAFANA_ADMIN_PASSWORD manquant", file=sys.stderr)
            return 2
        api = Grafana(password)
        _, users = api.request("GET", "/api/org/users")
        by_login = {u.get("login"): u for u in users}
        required = {name: by_login.get(name) for name in ("alice", "bob", "charlie")}
        missing = [name for name, user in required.items() if not user]
        if missing:
            raise RuntimeError("Utilisateur Grafana manquant : " + ", ".join(missing))
        for name, user in required.items():
            print(f"Role {name}: {user.get('role')}")
        dev_team = ensure_team(api, "nova-dev")
        rh_team = ensure_team(api, "nova-rh")
        ensure_member(api, dev_team["id"], "nova-dev", required["bob"]["userId"], "bob")
        ensure_member(api, rh_team["id"], "nova-rh", required["alice"]["userId"], "alice")
        dev_folder = ensure_folder(api, "nova-dev", "Dev")
        rh_folder = ensure_folder(api, "nova-rh", "RH")
        ensure_dashboard(api, "nova-services-iam", "Nova Services — Démonstration IAM", "Tableau de bord du laboratoire Nova Services")
        ensure_dashboard(api, "nova-dev-iam", "Nova Dev — IAM Test", "Espace Dev Nova Services", dev_folder["uid"])
        ensure_dashboard(api, "nova-rh-iam", "Nova RH — IAM Test", "Espace RH Nova Services", rh_folder["uid"])
        set_folder_permissions(api, dev_folder["uid"], dev_team["id"], "nova-dev", 2, required["charlie"]["userId"])
        set_folder_permissions(api, rh_folder["uid"], rh_team["id"], "nova-rh", 1, required["charlie"]["userId"])
        print("Préparation Grafana RBAC terminée (tests d'accès encore manuels).")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

