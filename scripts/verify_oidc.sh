#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
fail=0
ok() { echo "[OK] $1"; }
bad() { echo "[FAIL] $1${2:+ — $2}"; fail=1; }

discovery=$(curl -fsS http://localhost:9000/application/o/grafana/.well-known/openid-configuration 2>/dev/null || true)
if [[ -n "$discovery" ]]; then ok "Provider OIDC / application Authentik présents"; else bad "Provider OIDC / application Authentik" "discovery inaccessible"; fi
for key in issuer authorization_endpoint token_endpoint userinfo_endpoint jwks_uri; do
  if printf '%s' "$discovery" | python3 -c "import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get('$key') else 1)" 2>/dev/null; then ok "Discovery $key"; else bad "Discovery $key"; fi
done

if docker compose ps --status running --services 2>/dev/null | grep -qx grafana; then ok "Grafana démarré"; else bad "Grafana démarré"; fi
if curl -fsS http://localhost:3000/api/health 2>/dev/null | grep -Eq '"database"[[:space:]]*:[[:space:]]*"ok"'; then ok "Grafana health"; else bad "Grafana health"; fi

check_env() {
  local name="$1" expected="$2"
  if docker compose exec -T grafana sh -c "test \"\${$name:-}\" = \"$expected\"" >/dev/null 2>&1; then ok "$name"; else bad "$name"; fi
}
check_env GF_AUTH_GENERIC_OAUTH_ENABLED true
check_env GF_AUTH_GENERIC_OAUTH_USE_PKCE true
check_env GF_AUTH_GENERIC_OAUTH_AUTH_URL 'http://localhost:9000/application/o/authorize/'
check_env GF_AUTH_GENERIC_OAUTH_TOKEN_URL 'http://authentik-server:9000/application/o/token/'
check_env GF_AUTH_GENERIC_OAUTH_API_URL 'http://authentik-server:9000/application/o/userinfo/'
check_env GF_AUTH_GENERIC_OAUTH_GROUPS_ATTRIBUTE_PATH nova_groups
check_env GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_STRICT true
check_env GF_AUTH_GENERIC_OAUTH_ALLOW_ASSIGN_GRAFANA_ADMIN false

# Presence checks only; values are deliberately never printed.
if docker compose exec -T grafana sh -c 'test -n "${GF_AUTH_GENERIC_OAUTH_CLIENT_ID:-}" && test -n "${GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET:-}"' >/dev/null 2>&1; then ok "Identifiants OIDC présents"; else bad "Identifiants OIDC présents"; fi
exit "$fail"

