# 土地承包明细 API 路由端点
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/contracts", tags=["土地承包明细"])


@router.get("", response_model=schemas.PaginatedResponse, summary="获取土地承包明细列表")
def list_contracts(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    db: Session = Depends(get_db),
):
    """获取土地承包明细列表，支持分页，按创建时间倒序排列"""
    total, items = crud.get_contracts(db, page=page, page_size=page_size)
    return schemas.PaginatedResponse(
        total=total, page=page, page_size=page_size, items=items
    )


@router.get("/search", response_model=schemas.PaginatedResponse, summary="模糊搜索土地承包明细")
def search_contracts(
    name: Optional[str] = Query(None, description="承包人姓名（模糊匹配）"),
    land_location: Optional[str] = Query(None, description="地块位置（模糊匹配）"),
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    db: Session = Depends(get_db),
):
    """通过承包人姓名和地块位置进行模糊搜索，支持分页"""
    total, items = crud.search_contracts(
        db, name=name, land_location=land_location, page=page, page_size=page_size
    )
    return schemas.PaginatedResponse(
        total=total, page=page, page_size=page_size, items=items
    )


@router.post(
    "",
    response_model=schemas.ContractResponse,
    status_code=201,
    summary="创建土地承包明细",
)
def create_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    """创建新的土地承包明细记录"""
    return crud.create_contract(db, contract)


@router.put("/{contract_id}", response_model=schemas.ContractResponse, summary="更新土地承包明细")
def update_contract(
    contract_id: int, contract: schemas.ContractUpdate, db: Session = Depends(get_db)
):
    """更新指定 ID 的土地承包明细（支持部分字段更新）"""
    db_contract = crud.update_contract(db, contract_id, contract)
    if not db_contract:
        raise HTTPException(status_code=404, detail=f"未找到 ID 为 {contract_id} 的土地承包明细")
    return db_contract


@router.delete("/{contract_id}", summary="删除土地承包明细")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """删除指定 ID 的土地承包明细"""
    success = crud.delete_contract(db, contract_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"未找到 ID 为 {contract_id} 的土地承包明细")
    return {"message": f"ID 为 {contract_id} 的土地承包明细已成功删除"}
