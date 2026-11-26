from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.pet_service import PetService


def get_pet_service(db: Session = Depends(get_db)) -> PetService:
    """路由层依赖：注入数据库会话并构建服务层对象。"""
    return PetService(db)
