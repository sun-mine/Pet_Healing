# Pet Healing Backend

后端基于 FastAPI + SQLAlchemy 2.0，采用「路由层 → 服务层 → 数据库层」分层架构。

## 目录结构

```
backend/
├── main.py                          # 应用入口
├── requirements.txt                 # Python 依赖
└── app/
    ├── __init__.py
    ├── api/                         # ① 路由层：接收请求、参数校验、调用服务层
    │   ├── __init__.py
    │   ├── deps.py                  # 依赖注入
    │   └── routes/
    │       ├── __init__.py          # 汇总所有路由为 api_router
    │       ├── health.py            # 健康检查接口
    │       └── pets.py              # 宠物增删改查接口
    ├── services/                    # ② 服务层：业务规则编排
    │   ├── __init__.py
    │   └── pet_service.py
    ├── db/                          # ③ 数据库层：Session、表结构、读写查询
    │   ├── __init__.py
    │   ├── base.py                  # ORM 模型基类
    │   ├── session.py               # 数据库引擎与会话
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── pet.py               # pets 表结构
    │   └── repositories/
    │       ├── __init__.py
    │       └── pet_repository.py    # pets 表的增删改查
    ├── schemas/                     # 接口数据结构（入参 / 出参）
    │   ├── __init__.py
    │   └── pet.py
    └── core/                        # 全局配置与通用能力
        ├── __init__.py
        ├── config.py                # 读取仓库根目录 .env
        └── exceptions.py            # 业务异常定义
```

## 文件作用

### 根目录

| 文件 | 作用 |
| --- | --- |
| `main.py` | 应用入口。创建 FastAPI 实例、注册 CORS、挂载 `/api` 路由、启动时建表、把业务异常统一转成 HTTP 响应，并支持 `python main.py` 直接启动。 |
| `requirements.txt` | 后端依赖：fastapi、uvicorn、pydantic-settings、sqlalchemy。 |

### app/api（路由层）

只做「收请求 → 校验 → 调服务 → 返回」，不写业务规则、不直接操作数据库。

| 文件 | 作用 |
| --- | --- |
| `deps.py` | 依赖注入。`get_pet_service()` 取出数据库会话并构造 `PetService`，供路由使用。 |
| `routes/__init__.py` | 汇总 `health`、`pets` 等子路由为统一的 `api_router`。 |
| `routes/health.py` | `GET /api/health` 健康检查。 |
| `routes/pets.py` | 宠物接口：列表、详情、新增、更新、删除，并声明 `response_model`。 |

### app/services（服务层）

只写业务规则，例如「宠物不存在返回 404」「局部更新只改传入字段」。不依赖 FastAPI，可被脚本或其他入口复用。

| 文件 | 作用 |
| --- | --- |
| `pet_service.py` | `PetService`：列表、查询、创建、更新、删除的业务编排；不存在时抛 `NotFoundError`；通过仓储访问数据库。 |

### app/db（数据库层）

只负责数据怎么存、怎么查，不包含业务判断。

| 文件 | 作用 |
| --- | --- |
| `base.py` | `Base`，所有 ORM 模型的基类（SQLAlchemy 2.0 `DeclarativeBase`）。 |
| `session.py` | 根据 `DATABASE_URL` 创建 engine、`SessionLocal`，并提供 `get_db()` 每请求一个会话；SQLite 时自动创建数据目录。 |
| `models/pet.py` | `Pet` ORM 模型，对应 `pets` 表（id、name、species、breed、age、created_at）。 |
| `models/__init__.py` | 导出模型，保证建表时所有表都被注册。 |
| `repositories/pet_repository.py` | `PetRepository`：`pets` 表的增删改查（select / get / add / commit）。 |

### app/schemas（数据结构）

接口的「数据形状」，负责校验与序列化，与数据库表结构解耦。

| 文件 | 作用 |
| --- | --- |
| `pet.py` | `PetCreate` 创建入参、`PetUpdate` 局部更新入参（全可选）、`PetRead` 出参（含 id、created_at，`from_attributes` 支持直接序列化 ORM 对象）。 |

### app/core（配置与通用）

| 文件 | 作用 |
| --- | --- |
| `config.py` | `Settings` 读取仓库根目录 `.env`（应用名、调试、端口、CORS、`DATABASE_URL`），默认数据库为 `backend/data/app.db`。 |
| `exceptions.py` | `AppError` 业务异常基类与 `NotFoundError`，由 `main.py` 统一转换为 HTTP 404。 |

> 各目录下的 `__init__.py` 用于将目录声明为 Python 包，并为对应层提供统一的导出。

## 请求链路

```
HTTP 请求
  → 路由层 app/api/routes/*      参数校验、调用服务
  → 服务层 app/services/*        业务规则
  → 数据库层 app/db/repositories 拼 SQL、读写
  → app/db/models + session      映射到数据库
响应：ORM 对象 → schemas.PetRead → JSON
```

## 接口一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 健康检查 |
| GET | `/api/pets` | 宠物列表 |
| GET | `/api/pets/{pet_id}` | 宠物详情 |
| POST | `/api/pets` | 新增宠物 |
| PATCH | `/api/pets/{pet_id}` | 更新宠物（只改传入字段） |
| DELETE | `/api/pets/{pet_id}` | 删除宠物 |

启动后可访问 `http://127.0.0.1:8000/docs` 查看自动生成的接口文档。

## 运行

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
