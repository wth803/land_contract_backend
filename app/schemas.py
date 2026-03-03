# Pydantic 请求/响应模型，含字段验证
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class ContractBase(BaseModel):
    """土地承包明细公共字段"""

    name: str
    land_location: str
    id_card: str
    phone: str
    area: float
    year: int
    remark: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """承包人姓名不能为空"""
        if not v or not v.strip():
            raise ValueError("承包人姓名不能为空")
        return v.strip()

    @field_validator("land_location")
    @classmethod
    def land_location_not_empty(cls, v: str) -> str:
        """地块位置不能为空"""
        if not v or not v.strip():
            raise ValueError("地块位置不能为空")
        return v.strip()

    @field_validator("id_card")
    @classmethod
    def validate_id_card(cls, v: str) -> str:
        """身份证号格式验证：前17位为数字，最后一位为数字或X/x"""
        pattern = r"^\d{17}[\dXx]$"
        if not re.match(pattern, v):
            raise ValueError("身份证号格式不正确，应为18位（前17位为数字，最后一位为数字或X）")
        return v.upper()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """联系电话：必须为11位纯数字"""
        if not re.match(r"^\d{11}$", v):
            raise ValueError("联系电话格式不正确，应为11位纯数字")
        return v

    @field_validator("area")
    @classmethod
    def area_positive(cls, v: float) -> float:
        """承包面积必须大于0"""
        if v <= 0:
            raise ValueError("承包面积必须大于0")
        return v

    @field_validator("year")
    @classmethod
    def year_in_range(cls, v: int) -> int:
        """承包年份必须在合理范围内"""
        if v < 1949 or v > 2100:
            raise ValueError("承包年份必须在 1949 ~ 2100 之间")
        return v


class ContractCreate(ContractBase):
    """创建土地承包明细的请求模型"""
    pass


class ContractUpdate(BaseModel):
    """更新土地承包明细的请求模型（所有字段可选，只更新传入的非 None 字段）"""

    name: Optional[str] = None
    land_location: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None
    area: Optional[float] = None
    year: Optional[int] = None
    remark: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("承包人姓名不能为空")
        return v.strip() if v else v

    @field_validator("land_location")
    @classmethod
    def land_location_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("地块位置不能为空")
        return v.strip() if v else v

    @field_validator("id_card")
    @classmethod
    def validate_id_card(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            pattern = r"^\d{17}[\dXx]$"
            if not re.match(pattern, v):
                raise ValueError("身份证号格式不正确，应为18位（前17位为数字，最后一位为数字或X）")
            return v.upper()
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^\d{11}$", v):
            raise ValueError("联系电话格式不正确，应为11位纯数字")
        return v

    @field_validator("area")
    @classmethod
    def area_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("承包面积必须大于0")
        return v

    @field_validator("year")
    @classmethod
    def year_in_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1949 or v > 2100):
            raise ValueError("承包年份必须在 1949 ~ 2100 之间")
        return v


class ContractResponse(ContractBase):
    """土地承包明细响应模型（含数据库自动生成字段）"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """分页响应模型"""

    total: int
    page: int
    page_size: int
    items: list[ContractResponse]
