#!/usr/bin/env python3
"""Prepare/restore Alice's temporary no-group access test."""
import argparse
import sys
from authentik_api import AuthentikAPI


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    group.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        api = AuthentikAPI()
        alice = api.user("alice")
        rh = api.group("RH")
        if not alice or not rh:
            raise RuntimeError("Alice ou RH introuvable")
        in_rh = api.has_membership(alice, "RH")
        print(f"alice -> RH: {'oui' if in_rh else 'non'}")
        if args.check:
            return 0
        if args.apply:
            if in_rh:
                api.remove_user(rh, alice)
            print("Alice retirée temporairement de RH (nouvelle connexion OAuth requise).")
        else:
            if not in_rh:
                api.add_user(rh, alice)
            print("Alice restaurée dans RH (nouvelle connexion OAuth requise).")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
