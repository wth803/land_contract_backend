# 认证模块：密码哈希、JWT 生成与验证、当前用户依赖
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY
from app.database import get_db

# 密码哈希上下文，使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer Token 提取器
bearer_scheme = HTTPBearer()


def _truncate_password(password: str) -> str:
    """将密码按 UTF-8 字节截断到 72 字节（bcrypt 算法限制）"""
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    """使用 bcrypt 对明文密码进行哈希（自动截断超过 72 字节的部分）"""
    return pwd_context.hash(_truncate_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配（同样截断以保持一致）"""
    return pwd_context.verify(_truncate_password(plain_password), hashed_password)


def create_access_token(data: dict) -> str:
    """生成 JWT Token，包含用户名（sub 字段）和过期时间（exp 字段）"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    从请求头 Authorization: Bearer <token> 中解析 JWT Token，
    查找对应用户并返回。Token 无效或用户不存在则返回 401。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
