from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="资源名称")
    description: str | None = Field(default=None, max_length=500, description="资源描述")
    price: Decimal = Field(..., ge=0, description="资源价格")


class ItemCreate(ItemBase):
    """创建资源请求模型。"""


class ItemUpdate(BaseModel):
    """部分更新资源请求模型（PATCH）。"""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal | None = Field(default=None, ge=0)


class ItemResponse(ItemBase):
    id: int = Field(..., ge=1)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ItemListResponse(BaseModel):
    total: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
    offset: int = Field(..., ge=0)
    data: list[ItemResponse]
