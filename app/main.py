from fastapi import FastAPI, HTTPException, Query, Response, status

from app.repository import ItemRepository
from app.schemas import Item, ItemCreate, ItemList, ItemUpdate

app = FastAPI(
    title="RESTful + OpenAPI FastAPI Template",
    version="1.0.0",
    summary="一个同时遵循 RESTful 风格和 OpenAPI 文档规范的示例项目",
    description=(
        "该项目展示了如何使用资源化 URL、正确的 HTTP 动词/状态码、"
        "统一响应模型，并由 FastAPI 自动生成 OpenAPI 文档。"
    ),
)

repository = ItemRepository()


@app.get("/health", tags=["system"], summary="健康检查")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/api/v1/items",
    response_model=ItemList,
    tags=["items"],
    summary="分页查询资源列表",
)
def list_items(
    limit: int = Query(10, ge=1, le=100, description="单页条数"),
    offset: int = Query(0, ge=0, description="偏移量"),
) -> ItemList:
    total, records = repository.list(limit=limit, offset=offset)
    return ItemList(total=total, limit=limit, offset=offset, data=records)


@app.post(
    "/api/v1/items",
    response_model=Item,
    tags=["items"],
    status_code=status.HTTP_201_CREATED,
    summary="创建资源",
)
def create_item(payload: ItemCreate) -> Item:
    return repository.create(payload)


@app.get(
    "/api/v1/items/{item_id}",
    response_model=Item,
    tags=["items"],
    summary="按 ID 查询资源",
)
def get_item(item_id: int) -> Item:
    item = repository.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return item


@app.patch(
    "/api/v1/items/{item_id}",
    response_model=Item,
    tags=["items"],
    summary="部分更新资源",
)
def patch_item(item_id: int, payload: ItemUpdate) -> Item:
    item = repository.update(item_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return item


@app.delete(
    "/api/v1/items/{item_id}",
    tags=["items"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除资源",
)
def delete_item(item_id: int) -> Response:
    deleted = repository.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
