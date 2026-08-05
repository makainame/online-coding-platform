# 在线代码练习平台

基于 FastAPI + Vue 3 的在线代码练习平台 MVP，支持：

- 学生注册/登录、查看题目、在线编写 Python 代码
- 运行代码并执行测试用例
- 提交记录管理
- AI 反馈（可切换 DeepSeek / Qwen，未配置 Key 时使用本地规则反馈）

## 本地启动

### 1. 后端

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

接口文档：http://127.0.0.1:8000/docs

首次启动会自动创建数据库并写入演示数据：

- 学生账号：`student` / `student123`
- 教师账号：`teacher` / `teacher123`

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

打开 http://127.0.0.1:5173

## 运行测试

```bash
cd backend
python -m pytest -q
```

测试会覆盖注册/登录、题目、提交判题、AI 反馈和教师权限。

## 自动验证

推送到 GitHub 后，`.github/workflows/ci.yml` 会自动运行：

- 后端：安装 `requirements-dev.txt` 后执行 `python -m pytest -q`
- 前端：执行 `npm ci` 后执行 `npm run build`

## 配置 AI

复制 `.env.example` 为 `.env`（后端运行目录下），填写 API Key 后设置：

```bash
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
```

或：

```bash
AI_PROVIDER=qwen
QWEN_API_KEY=your_key
```

未配置时自动使用本地规则生成反馈，不影响主流程演示。

## 当前 MVP 边界

- 代码执行默认使用本地 `subprocess`，适合开发测试
- Docker 部署可设置 `EXECUTION_MODE=docker`，使用容器沙箱并做资源限制
- 当前只支持 Python 代码执行
- 数据库默认使用 SQLite，生产环境切换为 MySQL

## 扩展多语言题库

项目已经预留多语言扩展口：

- 题目数据支持 `language` 字段，默认 `python`
- 后端执行器通过 `register_executor(language, fn)` 注册
- 前端 Monaco Editor 会根据题目语言自动切换

后续接入 Java、JavaScript、C++ 等语言时，只需要：

1. 在题目数据里设置对应的 `language`
2. 在 `backend/app/services/executor_registry.py` 注册新的执行器
3. 增加对应语言的测试用例

## 题库导入

教师登录后进入“题库管理”，可以粘贴 JSON 批量导入题目。

模板文件：[import_template.json](import_template.json)

JSON 结构：

```json
[
  {
    "title": "题目名称",
    "description": "题目描述",
    "language": "python",
    "difficulty": "easy",
    "tags": "标签1,标签2",
    "starter_code": "起始代码",
    "test_cases": [
      {
        "input": "输入",
        "expected_output": "期望输出",
        "is_sample": true
      }
    ]
  }
]
```

重复导入时，会根据 `title + language` 更新已有题目，不会重复创建。

## Ubuntu 24.04 部署

部署脚本和说明在 [deploy/ubuntu](deploy/ubuntu)：

```bash
bash deploy/ubuntu/setup_ubuntu.sh
cp deploy/ubuntu/.env.production.example .env
bash deploy/ubuntu/deploy.sh
```
