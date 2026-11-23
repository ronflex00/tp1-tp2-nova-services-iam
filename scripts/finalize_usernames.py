#!/usr/bin/env python3
"""Correct only the Nova Services usernames, preserving account data."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("AUTHENTIK_URL", "http://localhost:9000").rstrip("/")
TOKEN = os.environ.get("AUTHENTIK_API_TOKEN")
TARGETS = {
    "alice@nova-services.test": "alice",
    "bob@nova-services.test": "bob",
    "charlie@nova-services.test": "charlie",
}


def request(token: str, method: str, path: str, payload: dict | None = None, query: dict | None = None):
    url = BASE + path
    if query:
        url += "?" + urlencode(query)
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not TOKEN:
        print("AUTHENTIK_API_TOKEN manquant", file=sys.stderr)
        return 2
    try:
        users = request(TOKEN, "GET", "/api/v3/core/users/", query={"page_size": 100})["results"]
        by_email = {u.get("email"): u for u in users if u.get("email")}
        for email, desired in TARGETS.items():
            user = by_email.get(email)
            if not user:
                raise RuntimeError(f"Compte introuvable pour {email}")
            current = user.get("username")
            if current == desired:
                print(f"{desired}: OK")
            elif args.check:
                print(f"{email}: username à corriger")
            else:
                request(TOKEN, "PATCH", f"/api/v3/core/users/{user['pk']}/", {"username": desired})
                print(f"{email}: username corrigé")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

