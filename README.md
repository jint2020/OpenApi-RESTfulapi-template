# OpenApi-RESTfulapi-template

这是一个基于 **Python + FastAPI + SQLAlchemy + PostgreSQL** 的模板项目，重点演示：

- **RESTful API 设计规范**（接口风格）
- **OpenAPI 规范**（接口描述标准）
- **RFC 7807 Problem Details** 错误响应规范
- 工程化目录结构与 Docker 一键启动

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
- 统一分页、过滤、版本化规则

### OpenAPI 是“描述标准”
OpenAPI 关注的是 API 如何被标准化描述：

- 路由、参数、请求体、响应体
- Schema（字段类型、约束、说明）
- 错误响应结构
- 标签、摘要、示例

FastAPI 会根据类型注解与模型自动生成 OpenAPI 文档（`/docs`、`/redoc`、`/openapi.json`）。

### 一句话理解
- RESTful：**怎么设计 API**
- OpenAPI：**怎么描述 API**

---

## 2. 工程结构（清晰化）

```bash
.
├── app
│   ├── api
│   │   ├── router.py                 # API 总路由
│   │   └── v1/endpoints/items.py     # v1 资源路由
│   ├── core
│   │   ├── config.py                 # 配置管理
│   │   └── errors.py                 # RFC 7807 全局异常处理
│   ├── db
│   │   ├── base.py                   # SQLAlchemy Base
│   │   └── session.py                # Engine/Session 依赖
│   ├── models
│   │   └── item.py                   # ORM 模型
│   ├── repositories
│   │   └── item_repository.py        # 数据访问层
│   ├── schemas
│   │   ├── item.py                   # 请求/响应模型
│   │   └── problem.py                # Problem Details 模型
│   └── main.py                       # 应用入口
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 3. 本地启动（PostgreSQL 持久化）

1) 启动 PostgreSQL（本机或容器）
2) 配置环境变量（可复制 `.env.example` 为 `.env`）
3) 安装依赖并启动：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## 4. Docker 一键启动

```bash
docker compose up --build
```

服务说明：

- API: `http://127.0.0.1:8000`
- PostgreSQL: `localhost:5432`

---

## 5. RESTful 接口示例

- `GET /health`：健康检查
- `GET /api/v1/items?limit=10&offset=0`：分页列表
- `POST /api/v1/items`：创建资源
- `GET /api/v1/items/{item_id}`：查询单个资源
- `PATCH /api/v1/items/{item_id}`：局部更新
- `DELETE /api/v1/items/{item_id}`：删除资源

---

## 6. RFC 7807 错误响应示例

当参数错误或资源不存在时，返回 `application/problem+json`：

```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Request payload or parameters failed validation.",
  "instance": "/api/v1/items",
  "invalid_params": [
    {
      "name": "body.price",
      "reason": "Input should be greater than or equal to 0"
    }
  ]
}
```

---

## 7. 规范落地说明

1. **资源化路径**：统一使用名词资源和版本前缀。
2. **语义化动词与状态码**：遵循标准 HTTP 语义。
3. **持久化层分离**：路由层、模型层、仓储层分离。
4. **文档自动化**：Schema 驱动 OpenAPI 自动生成。
5. **统一错误模型**：使用 RFC 7807 提高可观测性和一致性。
