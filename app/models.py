# SQLAlchemy ORM 数据模型
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Contract(Base):
    """土地承包明细数据表模型"""

    __tablename__ = "contracts"

    # 主键，自增整数
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 承包人姓名，不能为空
    name = Column(String(50), nullable=False, index=True)
    # 地块位置，不能为空
    land_location = Column(String(200), nullable=False, index=True)
    # 身份证号，18位
    id_card = Column(String(18), nullable=False)
    # 联系电话，11位纯数字
    phone = Column(String(11), nullable=False)
    # 承包面积（亩），必须大于0
    area = Column(Float, nullable=False)
    # 承包年份
    year = Column(Integer, nullable=False)
    # 村别，不能为空
    village = Column(String(50), nullable=False)
    # 银行卡号，可选
    bank_account = Column(String(25), nullable=True)
    # 承包方编码，不能为空
    contractor_code = Column(String(30), nullable=False)
    # 地块编码，不能为空
    plot_code = Column(String(30), nullable=False)
    # 备注，可选
    remark = Column(Text, nullable=True)
    # 创建时间，自动生成
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    # 更新时间，每次更新自动刷新
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class User(Base):
    """用户数据表模型"""

    __tablename__ = "users"

    # 主键，自增整数
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 用户名，唯一，不能为空
    username = Column(String(50), unique=True, nullable=False, index=True)
    # 哈希后的密码，不能为空
    hashed_password = Column(Text, nullable=False)
    # 是否激活，默认 True
    is_active = Column(Boolean, default=True, nullable=False)
    # 创建时间，自动生成
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
