from typing import List

from fastapi import APIRouter, Depends, status

from app.api.deps import get_pet_service
from app.schemas.pet import PetCreate, PetRead, PetUpdate
from app.services.pet_service import PetService

router = APIRouter(prefix="/pets", tags=["宠物"])


@router.get("", response_model=List[PetRead], summary="宠物列表")
def list_pets(service: PetService = Depends(get_pet_service)):
    return service.list_pets()


@router.get("/{pet_id}", response_model=PetRead, summary="宠物详情")
def get_pet(pet_id: int, service: PetService = Depends(get_pet_service)):
    return service.get_pet(pet_id)


@router.post(
    "",
    response_model=PetRead,
    status_code=status.HTTP_201_CREATED,
    summary="新增宠物",
)
def create_pet(payload: PetCreate, service: PetService = Depends(get_pet_service)):
    return service.create_pet(payload)


@router.patch("/{pet_id}", response_model=PetRead, summary="更新宠物")
def update_pet(
    pet_id: int,
    payload: PetUpdate,
    service: PetService = Depends(get_pet_service),
):
    return service.update_pet(pet_id, payload)


@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除宠物",
)
def delete_pet(pet_id: int, service: PetService = Depends(get_pet_service)):
    service.delete_pet(pet_id)
