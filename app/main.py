# FastAPI 应用入口：CORS 配置、全局异常处理、路由注册
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers import contracts

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时自动创建数据库表"""
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表已就绪")
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
