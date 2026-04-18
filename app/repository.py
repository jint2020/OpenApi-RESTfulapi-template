from __future__ import annotations

from datetime import datetime, timezone

from app.schemas import Item, ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self) -> None:
        self._data: dict[int, Item] = {}
        self._counter = 0

    def list(self, limit: int, offset: int) -> tuple[int, list[Item]]:
        records = sorted(self._data.values(), key=lambda x: x.id)
        return len(records), records[offset : offset + limit]

    def get(self, item_id: int) -> Item | None:
        return self._data.get(item_id)

    def create(self, payload: ItemCreate) -> Item:
        self._counter += 1
        now = datetime.now(timezone.utc)
        item = Item(id=self._counter, created_at=now, updated_at=now, **payload.model_dump())
        self._data[item.id] = item
        return item

    def update(self, item_id: int, payload: ItemUpdate) -> Item | None:
        existing = self._data.get(item_id)
        if not existing:
            return None

        values = payload.model_dump(exclude_unset=True)
        if not values:
            return existing

        updated = existing.model_copy(update={**values, "updated_at": datetime.now(timezone.utc)})
        self._data[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        if item_id in self._data:
            del self._data[item_id]
            return True
        return False
