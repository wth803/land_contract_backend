# 认证路由：登录、获取当前用户信息
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.auth import create_access_token, get_current_user, verify_password
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=schemas.LoginResponse, summary="用户登录")
def login(login_req: schemas.LoginRequest, db: Session = Depends(get_db)):
    """验证用户名和密码，成功后返回 JWT Access Token"""
    user = db.query(User).filter(User.username == login_req.username).first()
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return schemas.LoginResponse(
        access_token=access_token,
        username=user.username,
    )


@router.get("/me", response_model=schemas.UserResponse, summary="获取当前登录用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """返回当前登录用户的基本信息"""
    return current_user
