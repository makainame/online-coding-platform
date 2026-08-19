#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(pwd)}"

if [[ ! -f "$APP_DIR/.env" ]]; then
  echo "错误：$APP_DIR/.env 不存在"
  echo "请先执行：cp deploy/ubuntu/.env.production.example .env"
  exit 1
fi

cd "$APP_DIR"

echo "==> 清理 Docker 构建缓存，避免磁盘占满"
docker builder prune -f || true

echo "==> 构建并启动服务"
docker compose up -d --build

echo "==> 刷新前端代理，避免后端容器 IP 变化后仍请求旧地址"
docker compose restart frontend

echo "==> 服务状态"
docker compose ps

echo "==> 本地访问"
echo "前端:  http://127.0.0.1:8080"
echo "后端:  http://127.0.0.1:8000"
