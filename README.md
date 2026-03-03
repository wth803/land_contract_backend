# 土地承包明细管理系统后端

基于 FastAPI 框架开发的土地承包明细管理 RESTful API，支持土地承包信息的增删改查。

## 项目文件结构

```
land_contract_backend/
├── app/
│   ├── __init__.py              # 包初始化
│   ├── main.py                  # FastAPI 应用入口（CORS、全局异常处理）
│   ├── config.py                # 数据库连接配置（读取环境变量）
│   ├── database.py              # 数据库引擎和会话管理
│   ├── models.py                # SQLAlchemy ORM 数据模型
│   ├── schemas.py               # Pydantic 请求/响应模型（含数据验证）
│   ├── crud.py                  # 数据库 CRUD 操作封装
│   └── routers/
│       ├── __init__.py          # 路由包初始化
│       └── contracts.py         # 土地承包明细 API 路由端点
├── sql/
│   └── create_tables.sql        # PostgreSQL 建表脚本
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例文件
└── README.md                    # 项目文档
```

## 环境配置

1. 复制 `.env.example` 为 `.env`，填写实际数据库连接信息：

```bash
cp .env.example .env
```

`.env` 文件内容示例：

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_NAME=land_contract
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库（可选）

也可直接运行应用，应用启动时会自动创建数据库表。如需手动执行 SQL 脚本：

```bash
psql -U postgres -d land_contract -f sql/create_tables.sql
```

### 3. 启动应用

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 文档（Swagger UI）：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

## API 端点说明

| 方法   | 路径                      | 功能                             |
|--------|---------------------------|----------------------------------|
| GET    | `/`                       | 健康检查，返回应用基本信息       |
| GET    | `/api/contracts`          | 获取土地承包明细列表（支持分页） |
| GET    | `/api/contracts/search`   | 通过姓名和地块位置模糊搜索       |
| POST   | `/api/contracts`          | 创建新的土地承包明细             |
| PUT    | `/api/contracts/{id}`     | 更新现有土地承包明细（部分更新） |
| DELETE | `/api/contracts/{id}`     | 删除特定土地承包明细             |

### 分页参数

- `page`：页码，从 1 开始，默认 1
- `page_size`：每页条数，默认 10，最大 100

## API 使用示例（curl）

### 健康检查

```bash
curl http://localhost:8000/
```

### 获取列表（第1页，每页10条）

```bash
curl "http://localhost:8000/api/contracts?page=1&page_size=10"
```

### 模糊搜索

```bash
curl "http://localhost:8000/api/contracts/search?name=张&land_location=东村"
```

### 创建记录

```bash
curl -X POST http://localhost:8000/api/contracts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "land_location": "东村一组001号地块",
    "id_card": "110101199001011234",
    "phone": "13800138000",
    "area": 5.5,
    "year": 2023,
    "remark": "旱地"
  }'
```

### 更新记录（部分更新）

```bash
curl -X PUT http://localhost:8000/api/contracts/1 \
  -H "Content-Type: application/json" \
  -d '{"area": 6.0, "remark": "已灌溉水田"}'
```

### 删除记录

```bash
curl -X DELETE http://localhost:8000/api/contracts/1
```

## 数据验证规则

| 字段            | 规则                                        |
|-----------------|---------------------------------------------|
| `name`          | 不能为空                                    |
| `land_location` | 不能为空                                    |
| `id_card`       | 18位，前17位为数字，最后一位为数字或 X      |
| `phone`         | 11位纯数字                                  |
| `area`          | 浮点数，必须大于 0                          |
| `year`          | 整数，范围 1949 ~ 2100                      |
| `remark`        | 可选                                        |

## 注意事项

- **CORS**：开发环境配置允许所有来源（`allow_origins=["*"]`），生产环境请修改为具体的前端域名。
- **数据库**：应用启动时会自动调用 `Base.metadata.create_all` 创建表，无需手动执行 SQL（也可使用 `sql/create_tables.sql` 手动初始化）。
- **身份证号**：存储时末位字母统一转为大写。
- **更新接口**：只更新请求体中提供的非 `null` 字段，未传入的字段保持不变。