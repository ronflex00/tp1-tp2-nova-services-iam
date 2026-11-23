#!/usr/bin/env python3
"""Create the local secret file once, without ever printing secret values."""
from pathlib import Path
import os
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"

def main() -> int:
    for directory in ("data/authentik/media", "custom-templates", "certs", "docs", "captures", "backups"):
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print("REFUS : .env existe deja. Aucun secret n'a ete modifie.", file=sys.stderr)
        return 1
    content = "\n".join([
        f"POSTGRES_PASSWORD={secrets.token_hex(32)}",
        f"AUTHENTIK_SECRET_KEY={secrets.token_hex(32)}",
        f"GRAFANA_ADMIN_PASSWORD={secrets.token_hex(24)}",
        "",
    ])
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.chmod(ENV_FILE, 0o600)
    except Exception:
        try:
            ENV_FILE.unlink()
        except OSError:
            pass
        raise
    print("[OK] .env cree avec des secrets aleatoires (valeurs non affichees).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

