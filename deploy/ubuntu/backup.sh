#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(pwd)}"
BACKUP_DIR="${BACKUP_DIR:-$APP_DIR/backups}"

if [[ ! -f "$APP_DIR/.env" ]]; then
  echo "错误：$APP_DIR/.env 不存在" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"
cd "$APP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/coding_platform_$TIMESTAMP.sql"

docker compose exec -T mysql sh -c 'exec mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' > "$BACKUP_FILE"

echo "备份完成：$BACKUP_FILE"
