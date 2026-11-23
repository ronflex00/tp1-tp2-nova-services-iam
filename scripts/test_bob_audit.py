#!/usr/bin/env python3
"""Prepare/restore Bob's Dev -> Audit role transition; never changes credentials."""
import argparse
import sys
from authentik_api import AuthentikAPI, require_user_and_group


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    group.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        api = AuthentikAPI()
        bob = api.user("bob")
        dev = api.group("Dev")
        audit = api.group("Audit")
        if not bob or not dev or not audit:
            raise RuntimeError("Bob, Dev ou Audit introuvable")
        in_dev = api.has_membership(bob, "Dev")
        in_audit = api.has_membership(bob, "Audit")
        print(f"bob -> Dev: {'oui' if in_dev else 'non'}")
        print(f"bob -> Audit: {'oui' if in_audit else 'non'}")
        if args.check:
            return 0
        if args.apply:
            if in_dev:
                api.remove_user(dev, bob)
            if not in_audit:
                api.add_user(audit, bob)
            print("Bob préparé pour le test Audit (nouvelle connexion OAuth requise).")
        else:
            if in_audit:
                api.remove_user(audit, bob)
            if not in_dev:
                api.add_user(dev, bob)
            print("Bob restauré dans Dev (nouvelle connexion OAuth requise).")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
