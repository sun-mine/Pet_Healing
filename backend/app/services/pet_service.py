from typing import Sequence

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.models.pet import Pet
from app.db.repositories.pet_repository import PetRepository
from app.schemas.pet import PetCreate, PetUpdate


class PetService:
    """业务层：编排业务规则，通过仓储（数据库层）读写数据。"""

    def __init__(self, db: Session) -> None:
        self.repo = PetRepository(db)

    def list_pets(self) -> Sequence[Pet]:
        return self.repo.list()

    def get_pet(self, pet_id: int) -> Pet:
        pet = self.repo.get(pet_id)
        if pet is None:
            raise NotFoundError(f"宠物 {pet_id} 不存在")
        return pet

    def create_pet(self, payload: PetCreate) -> Pet:
        return self.repo.create(payload.model_dump())

    def update_pet(self, pet_id: int, payload: PetUpdate) -> Pet:
        pet = self.get_pet(pet_id)
        data = payload.model_dump(exclude_unset=True)
        if not data:
            return pet
        return self.repo.update(pet, data)

    def delete_pet(self, pet_id: int) -> None:
        pet = self.get_pet(pet_id)
        self.repo.delete(pet)
