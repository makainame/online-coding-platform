#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(pwd)}"
RESTORE_FILE="${1:-}"

if [[ -z "$RESTORE_FILE" ]]; then
  echo "用法：bash restore.sh backups/coding_platform_20260805_120000.sql" >&2
  exit 1
fi

if [[ ! -f "$RESTORE_FILE" ]]; then
  echo "备份文件不存在：$RESTORE_FILE" >&2
  exit 1
fi

cd "$APP_DIR"
docker compose exec -T mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' < "$RESTORE_FILE"

echo "恢复完成：$RESTORE_FILE"
