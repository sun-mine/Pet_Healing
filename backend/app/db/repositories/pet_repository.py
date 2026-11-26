from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.pet import Pet


class PetRepository:
    """数据库层：只负责 pets 表的读写与查询，不包含业务规则。"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> Sequence[Pet]:
        return self.db.scalars(select(Pet).order_by(Pet.id)).all()

    def get(self, pet_id: int) -> Optional[Pet]:
        return self.db.get(Pet, pet_id)

    def create(self, data: dict) -> Pet:
        pet = Pet(**data)
        self.db.add(pet)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def update(self, pet: Pet, data: dict) -> Pet:
        for field, value in data.items():
            setattr(pet, field, value)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def delete(self, pet: Pet) -> None:
        self.db.delete(pet)
        self.db.commit()
