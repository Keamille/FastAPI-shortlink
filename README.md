# FastAPI 短链接微服务

基于 **FastAPI + Redis** 的轻量长链转短链服务，配套 **Vue 3 + TypeScript** 管理端，适合练习前后端分离。

> 仓库已搭好前后端骨架与开发文档；业务逻辑（短链 CRUD、跳转、页面联调）按 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) 自行实现。

## 技术栈

| 层级 | 选型 |
|------|------|
| 后端 | FastAPI、Uvicorn、Pydantic Settings |
| 存储 | Redis only（无 PostgreSQL） |
| 短码 | Redis `INCR` + Base62（最短 6 位） |
| 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia |

## 仓库结构

```text
FastAPI-shortlink/
├── backend/          # FastAPI 模板（health / ping 可用，业务接口待实现）
│   └── .venv/        # 本地虚拟环境（已 gitignore）
├── frontend/         # Vue3 + TS 管理端模板
├── docs/
│   └── DEVELOPMENT.md
├── docker-compose.yml
└── README.md
```

## 完整开发文档

**[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** — 架构、Redis、API、联调与验收。

## 快速开始

```bash
# 1. Redis
docker compose up -d redis

# 2. 后端（虚拟环境已可按下列命令重建）
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
pip install -r requirements.txt
copy .env.example .env                # 若尚无 .env
uvicorn app.main:app --reload --port 8000

# 3. 前端（另开终端）
cd frontend
npm install
copy .env.example .env
npm run dev
```

- Swagger：`http://localhost:8000/docs`
- Health：`http://localhost:8000/health`
- 管理端：`http://localhost:5173`

## 你需要自己实现的部分

- 后端：`services/base62.py`、`services/shortlink.py`，以及 `api/links.py` / `api/redirect.py` 中的业务
- 前端：三个 View 里对接 `src/api/links.ts`
- Redis 连接注入（`deps.py` + `main.py` lifespan）

## 架构一览

```text
浏览器 ──► Vue 管理端 ──REST/JSON──► FastAPI ──► Redis
浏览器 ──► GET /{code} ───────────► FastAPI ──► Redis ──► 302 长链
```
