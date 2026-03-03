# 数据库 CRUD 操作封装
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas


def get_contracts(db: Session, page: int = 1, page_size: int = 10):
    """
    获取土地承包明细列表，支持分页，按 created_at 倒序排列
    """
    offset = (page - 1) * page_size
    total = db.query(func.count(models.Contract.id)).scalar()
    items = (
        db.query(models.Contract)
        .order_by(models.Contract.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return total, items


def search_contracts(
    db: Session,
    name: Optional[str] = None,
    land_location: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """
    通过姓名和土地位置模糊搜索，支持分页，按 created_at 倒序排列
    """
    query = db.query(models.Contract)
    if name:
        query = query.filter(models.Contract.name.ilike(f"%{name}%"))
    if land_location:
        query = query.filter(models.Contract.land_location.ilike(f"%{land_location}%"))
    total = query.with_entities(func.count(models.Contract.id)).scalar()
    items = (
        query.order_by(models.Contract.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items


def get_contract(db: Session, contract_id: int) -> Optional[models.Contract]:
    """根据 ID 获取单条土地承包明细"""
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()


def create_contract(db: Session, contract: schemas.ContractCreate) -> models.Contract:
    """创建新的土地承包明细"""
    db_contract = models.Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def update_contract(
    db: Session, contract_id: int, contract: schemas.ContractUpdate
) -> Optional[models.Contract]:
    """
    更新土地承包明细，只更新传入的非 None 字段（部分更新）
    """
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        return None
    update_data = contract.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(db_contract, field, value)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def delete_contract(db: Session, contract_id: int) -> bool:
    """删除指定 ID 的土地承包明细，返回是否成功"""
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        return False
    db.delete(db_contract)
    db.commit()
    return True
