from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, limit: int, offset: int) -> tuple[int, list[Item]]:
        total = self.db.query(Item).count()
        records = self.db.execute(select(Item).order_by(Item.id).offset(offset).limit(limit)).scalars().all()
        return total, records

    def get(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def create(self, payload: ItemCreate) -> Item:
        obj = Item(**payload.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, item_id: int, payload: ItemUpdate) -> Item | None:
        obj = self.db.get(Item, item_id)
        if not obj:
            return None

        values = payload.model_dump(exclude_unset=True)
        for key, value in values.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int) -> bool:
        obj = self.db.get(Item, item_id)
        if not obj:
            return False

        self.db.delete(obj)
        self.db.commit()
        return True
