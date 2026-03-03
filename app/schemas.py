# Pydantic 请求/响应模型，含字段验证
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator


class ContractBase(BaseModel):
    """土地承包明细公共字段"""

    name: str
    land_location: str
    id_card: str
    phone: str
    area: float
    year: int
    village: str
    bank_account: Optional[str] = None
    contractor_code: str
    plot_code: str
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

    @field_validator("village")
    @classmethod
    def village_not_empty(cls, v: str) -> str:
        """村别不能为空，最多50个字符"""
        if not v or not v.strip():
            raise ValueError("村别不能为空")
        if len(v.strip()) > 50:
            raise ValueError("村别最多50个字符")
        return v.strip()

    @field_validator("bank_account")
    @classmethod
    def validate_bank_account(cls, v: Optional[str]) -> Optional[str]:
        """银行卡号可选，长度在10-25位之间"""
        if v is not None and v.strip():
            stripped = v.strip()
            if not (10 <= len(stripped) <= 25):
                raise ValueError("银行卡号长度应在10到25位之间")
            return stripped
        return v

    @field_validator("contractor_code")
    @classmethod
    def contractor_code_not_empty(cls, v: str) -> str:
        """承包方编码不能为空，最多30个字符"""
        if not v or not v.strip():
            raise ValueError("承包方编码不能为空")
        if len(v.strip()) > 30:
            raise ValueError("承包方编码最多30个字符")
        return v.strip()

    @field_validator("plot_code")
    @classmethod
    def plot_code_not_empty(cls, v: str) -> str:
        """地块编码不能为空，最多30个字符"""
        if not v or not v.strip():
            raise ValueError("地块编码不能为空")
        if len(v.strip()) > 30:
            raise ValueError("地块编码最多30个字符")
        return v.strip()


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
    village: Optional[str] = None
    bank_account: Optional[str] = None
    contractor_code: Optional[str] = None
    plot_code: Optional[str] = None
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

    @field_validator("village")
    @classmethod
    def village_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("村别不能为空")
        if v is not None and len(v.strip()) > 50:
            raise ValueError("村别最多50个字符")
        return v.strip() if v is not None else None

    @field_validator("bank_account")
    @classmethod
    def validate_bank_account(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            stripped = v.strip()
            if not (10 <= len(stripped) <= 25):
                raise ValueError("银行卡号长度应在10到25位之间")
            return stripped
        return v

    @field_validator("contractor_code")
    @classmethod
    def contractor_code_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("承包方编码不能为空")
        if v is not None and len(v.strip()) > 30:
            raise ValueError("承包方编码最多30个字符")
        return v.strip() if v is not None else None

    @field_validator("plot_code")
    @classmethod
    def plot_code_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("地块编码不能为空")
        if v is not None and len(v.strip()) > 30:
            raise ValueError("地块编码最多30个字符")
        return v.strip() if v is not None else None


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


# 合法的可导出字段名
EXPORTABLE_FIELDS = {
    "name", "id_card", "phone", "land_location", "area", "year", "remark",
    "village", "bank_account", "contractor_code", "plot_code",
    "created_at", "updated_at",
}


class ExportRequest(BaseModel):
    """导出请求模型"""

    columns: List[str]  # 要导出的列
    search_name: Optional[str] = None  # 搜索条件：姓名
    search_land_location: Optional[str] = None  # 搜索条件：地块位置

    @field_validator("columns")
    @classmethod
    def columns_not_empty(cls, v: List[str]) -> List[str]:
        """columns 不能为空，且每个列名必须是合法字段名"""
        if not v:
            raise ValueError("columns 不能为空列表，请至少选择一列")
        invalid = [col for col in v if col not in EXPORTABLE_FIELDS]
        if invalid:
            raise ValueError(f"以下列名不合法：{invalid}，合法列名为：{sorted(EXPORTABLE_FIELDS)}")
        return v


class LoginRequest(BaseModel):
    """登录请求模型"""

    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_max_length(cls, v: str) -> str:
        """密码长度不能超过 72 字节（bcrypt 算法限制）"""
        if len(v.encode("utf-8")) > 72:
            raise ValueError("密码长度不能超过 72 字节")
        return v


class LoginResponse(BaseModel):
    """登录响应模型"""

    access_token: str
    token_type: str = "bearer"
    username: str


class UserResponse(BaseModel):
    """用户信息响应模型"""

    id: int
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
