from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate
from app.schemas.problem import ProblemDetails

router = APIRouter(prefix="/items", tags=["items"])

problem_responses = {
    404: {"model": ProblemDetails, "description": "资源不存在"},
    422: {"model": ProblemDetails, "description": "请求参数校验失败"},
    500: {"model": ProblemDetails, "description": "服务器内部错误"},
}


@router.get("", response_model=ItemListResponse, summary="分页查询资源列表", responses=problem_responses)
def list_items(
    limit: int = Query(10, ge=1, le=100, description="单页条数"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db),
) -> ItemListResponse:
    repo = ItemRepository(db)
    total, records = repo.list(limit=limit, offset=offset)
    return ItemListResponse(total=total, limit=limit, offset=offset, data=records)


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建资源",
    responses={422: problem_responses[422], 500: problem_responses[500]},
)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> ItemResponse:
    repo = ItemRepository(db)
    return repo.create(payload)


@router.get("/{item_id}", response_model=ItemResponse, summary="按 ID 查询资源", responses=problem_responses)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemResponse:
    repo = ItemRepository(db)
    item = repo.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return item


@router.patch("/{item_id}", response_model=ItemResponse, summary="部分更新资源", responses=problem_responses)
def patch_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)) -> ItemResponse:
    repo = ItemRepository(db)
    item = repo.update(item_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除资源",
    responses={404: problem_responses[404], 500: problem_responses[500]},
)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    repo = ItemRepository(db)
    deleted = repo.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
