# FastAPI 短链接微服务

基于 **FastAPI + Redis** 的长链转短链服务，配套 **Vue 3 + TypeScript** 管理端。

## 技术栈

| 层级 | 选型 |
|------|------|
| 后端 | FastAPI、Uvicorn、Pydantic Settings |
| 存储 | Redis（无 PostgreSQL） |
| 短码 | 默认 `INCR` + Base62；可选自定义短码 |
| 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia、Axios |

## 使用教程

### 环境要求

- Python 3.11+
- Node.js 18+
- Docker（用于启动 Redis）

### 1. 启动 Redis

在项目根目录：

```bash
docker compose up -d redis
```

若本机 `6379` 已有 Redis 在跑，可跳过此步。

### 2. 启动后端

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env          # Windows；Linux/macOS 用 cp
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 文档：http://localhost:8000/docs  
- 健康检查：http://localhost:8000/health  

### 3. 启动前端管理端

另开一个终端：

```bash
cd frontend
npm install
copy .env.example .env          # Windows；Linux/macOS 用 cp
npm run dev
```

浏览器打开：http://localhost:5173  

开发环境已配置 Vite 代理，将 `/api`、`/health` 转发到后端 `8000` 端口。

### 4. 基本使用

1. 在「创建」页填写长链接（可选手写短码、TTL）
2. 提交后复制生成的短链，浏览器打开应 302 跳转到原地址
3. 在「列表」查看、进入详情或删除短链

### 常用接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/links` | 创建短链（body: `url`，可选 `custom_code`、`ttl_seconds`） |
| GET | `/api/v1/links` | 分页列表 |
| GET | `/api/v1/links/{code}` | 详情 |
| DELETE | `/api/v1/links/{code}` | 删除 |
| GET | `/{code}` | 公开跳转（302） |
