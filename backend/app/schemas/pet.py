from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PetBase(BaseModel):
    name: str = Field(..., max_length=50, description="宠物名称")
    species: str = Field(..., max_length=30, description="物种，如 犬 / 猫")
    breed: Optional[str] = Field(default=None, max_length=50, description="品种")
    age: Optional[int] = Field(default=None, ge=0, le=100, description="年龄（岁）")


class PetCreate(PetBase):
    """创建宠物入参。"""


class PetUpdate(BaseModel):
    """更新宠物入参，字段均为可选，只更新传入的字段。"""

    name: Optional[str] = Field(default=None, max_length=50)
    species: Optional[str] = Field(default=None, max_length=30)
    breed: Optional[str] = Field(default=None, max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=100)


class PetRead(PetBase):
    """宠物出参。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
