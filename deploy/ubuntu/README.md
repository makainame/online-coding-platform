# Ubuntu 24.04 部署说明

## 1. 安装 Docker

在 Ubuntu 24.04 虚拟机中执行：

```bash
bash setup_ubuntu.sh
```

脚本会安装 Docker Engine、Docker Compose 插件，并把当前用户加入 `docker` 组。

## 2. 准备项目

```bash
git clone <你的仓库地址> coding-platform
cd coding-platform
cp deploy/ubuntu/.env.production.example .env
```

编辑 `.env`，至少修改：

- `MYSQL_ROOT_PASSWORD`
- `DATABASE_URL`
- `SECRET_KEY`
- 如果使用真实 AI，填写 `DEEPSEEK_API_KEY` 或 `QWEN_API_KEY`

## 3. Docker Hub 访问问题

国内网络下如果执行 `docker compose up -d --build` 时拉取镜像失败，提示类似：

```text
failed to resolve reference "docker.io/library/mysql:8.0": connection refused
```

先确认虚拟机外网正常：

```bash
curl -I --max-time 10 https://www.baidu.com
```

然后配置国内镜像源：

```bash
echo '{"registry-mirrors":["https://docker.m.daocloud.io","https://docker.1ms.run","https://docker.xuanyuan.me"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

测试镜像源：

```bash
docker pull mysql:8.0
```

如果后端 `pip install` 或前端 `npm install` 在构建时也超时，Dockerfile 已配置国内镜像：

- Python：清华 PyPI 镜像 `https://pypi.tuna.tsinghua.edu.cn/simple`
- Node：npmmirror `https://registry.npmmirror.com`

修改过 Dockerfile 后需要重新把项目或对应文件传到虚拟机，再执行：

```bash
bash deploy/ubuntu/deploy.sh
```

如果从 Windows 通过 `scp` 传项目，`node_modules` 也会被一起传过去，导致 Docker 前端构建报 `vite: Permission denied`。前端已增加 `.dockerignore` 排除 `node_modules`，重新传输 `frontend/.dockerignore` 后再构建即可。

## 4. 启动

```bash
bash deploy/ubuntu/deploy.sh
```

或者手动执行：

```bash
docker compose up -d --build
docker compose ps
```

启动后：

- 前端：http://127.0.0.1:8080
- 后端 API：http://127.0.0.1:8000
- 接口文档：http://127.0.0.1:8000/docs

## 从 Windows 浏览器访问

前端已映射到 `8080:80`。如果虚拟机 IP 是 `192.168.59.129`，在 Windows 浏览器打开：

```text
http://192.168.59.129:8080
```

如果打不开，在 Ubuntu 里开放防火墙端口：

```bash
sudo ufw allow 8080/tcp
```

## 5. Nginx 域名入口（可选）

```bash
sudo apt-get install -y nginx
sudo cp nginx.conf /etc/nginx/sites-available/coding-platform
sudo ln -s /etc/nginx/sites-available/coding-platform /etc/nginx/sites-enabled/coding-platform
sudo nginx -t
sudo systemctl reload nginx
```

把 `nginx.conf` 中的 `server_name` 改成真实域名。

## 6. HTTPS

域名解析到服务器后，可以使用 Certbot：

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 7. 运维命令

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
docker compose up -d --build
```

数据库数据保存在 Docker volume `mysql_data` 中，`docker compose down` 不会删除数据。
