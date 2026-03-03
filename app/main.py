# FastAPI 应用入口：CORS 配置、全局异常处理、路由注册
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.routers import contracts
from app.routers import auth

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时自动创建数据库表，并初始化默认管理员账户"""
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表已就绪")

    # 检查是否存在用户，若不存在则创建默认管理员
    from app.auth import hash_password
    from app.models import User

    db: Session = SessionLocal()
    try:
        if db.query(User).count() == 0:
            admin = User(
                username="admin",
                hashed_password=hash_password("admin123"),
                is_active=True,
            )
            db.add(admin)
            db.commit()
            logger.info("已创建默认管理员账户：用户名 admin，密码 admin123，请及时修改密码")
    finally:
        db.close()

    yield


# 创建 FastAPI 应用实例
app = FastAPI(
    title="土地承包明细管理系统",
    description="土地承包明细管理后端 RESTful API，支持土地承包信息的增删改查。",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置 CORS 跨域中间件
# 注意：开发环境允许所有来源，生产环境应将 allow_origins 修改为具体的前端域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请替换为前端实际域名，例如 ["https://your-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器：捕获未处理的异常并返回统一格式
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("未处理的异常: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误，请稍后重试"},
    )


# 注册路由
app.include_router(auth.router)
app.include_router(contracts.router)


# 健康检查端点
@app.get("/", summary="健康检查", tags=["系统"])
def health_check():
    """返回应用基本信息"""
    return {
        "app": "土地承包明细管理系统",
        "version": "1.0.0",
        "status": "running",
    }
