# 认证相关 API 路由端点：登录、获取当前用户信息
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import create_access_token, get_current_user, verify_password
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=schemas.LoginResponse, summary="用户登录")
def login(login_req: schemas.LoginRequest, db: Session = Depends(get_db)):
    """验证用户名和密码，成功返回 JWT Token"""
    user = db.query(models.User).filter(models.User.username == login_req.username).first()
    if not user or not user.is_active or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return schemas.LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
    )


@router.get("/me", response_model=schemas.UserResponse, summary="获取当前用户信息")
def get_me(current_user: models.User = Depends(get_current_user)):
    """返回当前登录用户的信息"""
    return current_user
