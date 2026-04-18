# OpenApi-RESTfulapi-template

这是一个基于 **Python + FastAPI** 的模板项目，用来演示如何同时遵循：

- **RESTful API 设计规范**（接口风格）
- **OpenAPI 规范**（接口文档描述标准）

---

## 1. OpenAPI 和 RESTful 的区别

### RESTful 是“设计风格”
RESTful 关注的是 API 怎么设计才符合资源化、语义化：

- URL 用名词表示资源（如 `/api/v1/items`）
- HTTP 方法表达动作：
  - `GET` 查询
  - `POST` 创建
  - `PATCH` 局部更新
  - `DELETE` 删除
- 使用合适的状态码（如 `201`、`404`、`204`）
- 常见能力：分页、过滤、版本化

### OpenAPI 是“描述标准”
OpenAPI 关注的是 API 如何被机器和人“标准化理解”：

- 接口路径与参数
- 请求/响应 schema
- 状态码与错误结构
- 标签、摘要、描述

FastAPI 会基于代码自动生成 OpenAPI 文档（Swagger UI / ReDoc）。

### 一句话理解
- RESTful：**你怎么设计 API**
- OpenAPI：**你怎么描述 API**

二者不是替代关系，而是互补关系。

---

## 2. 项目结构

```bash
.
├── app
│   ├── main.py          # 路由与应用入口
│   ├── repository.py    # 内存数据仓库（示例）
│   └── schemas.py       # Pydantic 请求/响应模型
├── requirements.txt
└── README.md
```

---

## 3. 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## 4. 示例接口（RESTful）

- `GET /health`：健康检查
- `GET /api/v1/items?limit=10&offset=0`：分页列表
- `POST /api/v1/items`：创建资源
- `GET /api/v1/items/{item_id}`：查询单个资源
- `PATCH /api/v1/items/{item_id}`：局部更新
- `DELETE /api/v1/items/{item_id}`：删除资源

---

## 5. 本模板如何体现规范

1. **资源化 URL**：采用 `/api/v1/items` 这种名词路径。
2. **语义化方法**：严格区分 GET/POST/PATCH/DELETE。
3. **状态码规范**：创建返回 `201`，删除返回 `204`，不存在返回 `404`。
4. **统一数据模型**：请求和响应都由 `Pydantic` schema 定义。
5. **自动文档**：FastAPI 自动生成 OpenAPI 文档，便于联调与 SDK 生成。

> 当前仓库使用内存存储，便于学习与演示。生产环境可替换为数据库（PostgreSQL / MySQL / MongoDB 等）。
