#!/usr/bin/env bash
set -euo pipefail

echo "==> 更新系统并安装 Docker 依赖"
sudo apt-get update
sudo apt-get install -y ca-certificates curl

echo "==> 添加 Docker 官方仓库"
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

docker --version
docker compose version

echo "==> 安装完成。当前用户已加入 docker 组，重新登录或新开 SSH 会话后生效。"

