from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.errors import add_exception_handlers
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        summary="一个遵循 RESTful 风格和 OpenAPI 规范的 FastAPI 项目模板",
        description="项目展示了清晰工程结构、PostgreSQL 持久化、以及 RFC 7807 错误响应。",
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/health", tags=["system"], summary="健康检查")
    def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    app.include_router(api_router)
    add_exception_handlers(app)
    return app


app = create_app()
