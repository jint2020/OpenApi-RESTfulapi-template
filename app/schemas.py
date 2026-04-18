from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="资源名称")
    description: Optional[str] = Field(default=None, max_length=500, description="资源描述")
    price: float = Field(..., ge=0, description="资源价格")


class ItemCreate(ItemBase):
    """创建资源时使用的请求模型。"""


class ItemUpdate(BaseModel):
    """部分更新资源时使用的请求模型（PATCH 语义）。"""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, ge=0)


class Item(ItemBase):
    id: int = Field(..., ge=1, description="资源唯一标识")
    created_at: datetime
    updated_at: datetime


class ItemList(BaseModel):
    total: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
    offset: int = Field(..., ge=0)
    data: list[Item]
