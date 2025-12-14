#!/usr/bin/env bash
set -euo pipefail

# resolve repo root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF_FILE="$ROOT_DIR/conf/bot.conf"
MASTER_SQL="$ROOT_DIR/conf/run_all.sql"

# ensure conf exists
if [[ ! -f "$CONF_FILE" ]]; then
  echo "Missing conf file: $CONF_FILE" >&2
  exit 1
fi

# Helper to read a key (supports quoted or unquoted values)
read_conf() {
  local key="$1"
  local val
  val=$(grep -E "^${key}=" "$CONF_FILE" | sed -E "s/^${key}=\"?([^\"]*)\"?/\1/") || true
  echo "$val"
}

# extract needed values
DB_PASS=$(read_conf DB_PASSWORD)
SSHUSR=$(read_conf SSHUSR)
S2=$(read_conf S2)
WEATHER_API_KEY=$(read_conf WEATHER_API_KEY)
BOT_KEY=$(read_conf BOT_KEY)
TIMEOUT=$(read_conf timeout)

# validate mandatory values
if [[ -z "$DB_PASS" ]]; then
  echo "DB_PASSWORD is empty or not set in $CONF_FILE" >&2
  exit 1
fi

# ensure master SQL exists
if [[ ! -f "$MASTER_SQL" ]]; then
  echo "Missing master SQL: $MASTER_SQL" >&2
  exit 1
fi

# build the MySQL prelude for session variables
# use NULL if a variable is not provided; COALESCE in SQL will default to ''
MYSQL_PRELUDE=$(cat <<EOF
SET @DB_PASSWORD := '${DB_PASS}';
SET @SSHUSR := ${SSHUSR:+"${SSHUSR}"};
SET @S2 := ${S2:+"${S2}"};
SET @WEATHER_API_KEY := ${WEATHER_API_KEY:+"${WEATHER_API_KEY}"};
SET @BOT_KEY := ${BOT_KEY:+"${BOT_KEY}"};
SET @timeout := ${TIMEOUT:+"${TIMEOUT}"};
EOF
)

# run MySQL sourcing with injected user variables
# root password will be prompted interactively by -p
mysql -u root -p -e "${MYSQL_PRELUDE} SOURCE $MASTER_SQL;"
