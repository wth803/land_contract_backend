# 数据库连接配置，从环境变量读取，支持 .env 文件
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 数据库连接参数
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "land_contract")

# 拼接 SQLAlchemy 数据库连接 URL
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# JWT 认证配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-to-a-random-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))
