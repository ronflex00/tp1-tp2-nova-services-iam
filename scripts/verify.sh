#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
fail=0
ok() { echo "[OK] $1"; }
bad() { echo "[FAIL] $1${2:+ — $2}"; fail=1; }
command -v docker >/dev/null && ok "Docker" || bad "Docker" "commande absente"
docker compose version >/dev/null 2>&1 && ok "Docker Compose" || bad "Docker Compose" "plugin indisponible"
python3 - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3,9) else 1)
PY
[[ $? -eq 0 ]] && ok "Python >= 3.9" || bad "Python >= 3.9"
[[ -f .env ]] && ok ".env présent" || bad ".env présent"
if docker compose config --quiet >/dev/null 2>&1; then ok "Configuration Compose"; else bad "Configuration Compose"; fi
expected=$'postgres\nauthentik-server\nauthentik-worker\ngrafana'
actual=$(docker compose config --services 2>/dev/null || true)
if diff -u <(printf '%s\n' "$expected" | sort) <(printf '%s\n' "$actual" | sort) >/dev/null; then ok "Quatre services attendus"; else bad "Quatre services attendus" "$actual"; fi
running=$(docker compose ps --status running --services 2>/dev/null || true)
if printf '%s\n' "$running" | sort | diff -u <(printf '%s\n' "$expected" | sort) - >/dev/null; then ok "Conteneurs démarrés"; else bad "Conteneurs démarrés" "démarrage incomplet"; fi
if printf '%s\n' "$running" | grep -qx postgres && docker compose exec -T postgres sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1;"' 2>/dev/null | grep -qx 1; then ok "PostgreSQL"; else bad "PostgreSQL"; fi
if printf '%s\n' "$running" | grep -qx authentik-server && curl -fsS http://localhost:9000/-/health/live/ >/dev/null 2>&1; then ok "Authentik Live"; else bad "Authentik Live"; fi
if printf '%s\n' "$running" | grep -qx authentik-server && curl -fsS http://localhost:9000/-/health/ready/ >/dev/null 2>&1; then ok "Authentik Ready"; else bad "Authentik Ready"; fi
if printf '%s\n' "$running" | grep -qx authentik-worker && docker compose exec -T authentik-worker ak healthcheck >/dev/null 2>&1; then ok "Authentik Worker"; else bad "Authentik Worker"; fi
if printf '%s\n' "$running" | grep -qx grafana && curl -fsS http://localhost:3000/api/health 2>/dev/null | grep -Eq '"database"[[:space:]]*:[[:space:]]*"ok"'; then ok "Grafana"; else bad "Grafana"; fi
exit "$fail"

