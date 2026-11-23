#!/usr/bin/env python3
"""Ensure the requested display names and business attributes without changing access data."""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = os.environ.get("AUTHENTIK_URL", "http://localhost:9000").rstrip("/")
TOKEN = os.environ.get("AUTHENTIK_API_TOKEN")
EXPECTED = {
    "alice@nova-services.test": ("Alice Martin", {"department": "RH", "role": "Manager RH", "clearance_level": 2}),
    "bob@nova-services.test": ("Bob Dupont", {"department": "Development", "role": "Backend Developer", "clearance_level": 1}),
    "charlie@nova-services.test": ("Charlie Bernard", {"department": "IT", "role": "System Administrator", "clearance_level": 5}),
}


def api(method: str, path: str, payload: dict | None = None, query: dict | None = None):
    url = BASE + path + (("?" + urlencode(query)) if query else "")
    body = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {TOKEN}", "Accept": "application/json", "Content-Type": "application/json",
    })
    try:
        with urlopen(req, timeout=20) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        raise RuntimeError(f"API {method} {path} HTTP {exc.code}") from None
    except URLError as exc:
        raise RuntimeError(f"API inaccessible sur {BASE}: {exc.reason}") from None


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not TOKEN:
        print("AUTHENTIK_API_TOKEN manquant", file=sys.stderr)
        return 2
    try:
        users = api("GET", "/api/v3/core/users/", query={"page_size": 100})["results"]
        by_email = {u.get("email"): u for u in users if u.get("email")}
        for email, (name, expected_attrs) in EXPECTED.items():
            user = by_email.get(email)
            if not user:
                raise RuntimeError(f"Compte introuvable pour {email}")
            current_attrs = dict(user.get("attributes") or {})
            merged_attrs = dict(current_attrs)
            merged_attrs.update(expected_attrs)
            needs = user.get("name") != name or current_attrs != merged_attrs
            if not needs:
                print(f"{email}: OK")
            elif args.check:
                print(f"{email}: nom/attributs à compléter")
            else:
                api("PATCH", f"/api/v3/core/users/{user['pk']}/", {"name": name, "attributes": merged_attrs})
                print(f"{email}: nom/attributs complétés")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

