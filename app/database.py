# 数据库引擎和会话管理
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂，每次请求使用独立会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 模型基类
class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI 依赖注入：提供数据库会话，请求结束后自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
