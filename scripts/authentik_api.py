"""Small secret-safe Authentik API helper used by lifecycle test scripts."""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = os.environ.get("AUTHENTIK_URL", "http://localhost:9000").rstrip("/")


class AuthentikAPI:
    def __init__(self):
        token = os.environ.get("AUTHENTIK_API_TOKEN")
        if not token:
            raise RuntimeError("AUTHENTIK_API_TOKEN manquant")
        self.headers = {"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}

    def request(self, method: str, path: str, payload=None, query=None):
        url = BASE + path + (("?" + urlencode(query)) if query else "")
        data = None if payload is None else json.dumps(payload).encode()
        req = Request(url, data=data, method=method, headers=self.headers)
        try:
            with urlopen(req, timeout=20) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except HTTPError as exc:
            raise RuntimeError(f"Authentik API {method} {path}: HTTP {exc.code}") from None
        except URLError as exc:
            raise RuntimeError(f"Authentik inaccessible sur {BASE}: {exc.reason}") from None

    def users(self):
        return self.request("GET", "/api/v3/core/users/", query={"page_size": 100, "include_groups": "true"}).get("results", [])

    def groups(self):
        return self.request("GET", "/api/v3/core/groups/", query={"page_size": 100}).get("results", [])

    def user(self, username: str):
        return next((u for u in self.users() if u.get("username") == username), None)

    def group(self, name: str):
        return next((g for g in self.groups() if g.get("name") == name), None)

    def has_membership(self, user: dict, group_name: str) -> bool:
        return any(g.get("name") == group_name for g in user.get("groups_obj") or [])

    def add_user(self, group: dict, user: dict):
        self.request("POST", f"/api/v3/core/groups/{group['pk']}/add_user/", {"pk": user["pk"]})

    def remove_user(self, group: dict, user: dict):
        self.request("POST", f"/api/v3/core/groups/{group['pk']}/remove_user/", {"pk": user["pk"]})


def require_user_and_group(api: AuthentikAPI, username: str, group_name: str):
    user = api.user(username)
    group = api.group(group_name)
    if not user:
        raise RuntimeError(f"Utilisateur introuvable : {username}")
    if not group:
        raise RuntimeError(f"Groupe introuvable : {group_name}")
    return user, group
