# Pet Healing Backend

后端骨架，基于 FastAPI + SQLAlchemy，按「路由层 → 服务层 → 数据库层」分层。
当前仅保留目录结构与各包的 `__init__.py`，业务代码待补充。

## 目录结构

```
backend/
├── README.md              # 本文档
├── requirements.txt       # Python 依赖清单
└── app/
    ├── __init__.py
    ├── api/               # ① 路由层
    │   ├── __init__.py
    │   └── routes/        #   各业务路由模块（如 pets.py、users.py）
    │       └── __init__.py
    ├── services/          # ② 服务层
    │   └── __init__.py
    ├── db/                # ③ 数据库层
    │   ├── __init__.py
    │   ├── models/        #   表结构（ORM 模型）
    │   │   └── __init__.py
    │   └── repositories/  #   数据读写（SQL 查询）
    │       └── __init__.py
    ├── schemas/           # 接口入参 / 出参的数据结构
    │   └── __init__.py
    └── core/              # 配置、异常等通用能力
        └── __init__.py
```

## 各层职责

| 目录 | 职责 | 允许依赖 |
| --- | --- | --- |
| `app/api/` | 路由层。接收 HTTP 请求、校验参数、调用服务层、返回响应；不写业务规则，不直接操作数据库。 | services、schemas |
| `app/services/` | 服务层。编排业务逻辑（判断、组合、事务边界），通过仓储访问数据库；不依赖 FastAPI。 | db、schemas |
| `app/db/models/` | 数据库层。ORM 表结构定义。 | core |
| `app/db/repositories/` | 数据库层。只负责增删改查，不含业务判断。 | models |
| `app/schemas/` | 接口数据结构。入参校验、出参裁剪与序列化，与表结构解耦。 | — |
| `app/core/` | 全局配置、业务异常、安全等通用能力。 | — |

## 新增一个资源的推荐顺序

以「宠物（pets）」为例：

1. `app/db/models/pet.py` —— 定义 `Pet` 表结构。
2. `app/db/repositories/pet_repository.py` —— 实现 `PetRepository` 的增删改查。
3. `app/schemas/pet.py` —— 定义 `PetCreate`、`PetUpdate`、`PetRead`。
4. `app/services/pet_service.py` —— `PetService` 编排业务规则，调用仓储。
5. `app/api/routes/pets.py` —— 定义接口，通过依赖注入拿到 `PetService`。
6. 在 `app/api/routes/__init__.py` 汇总路由，并在 `main.py` 中挂载到 `/api`。

`requirements.txt` 已包含 fastapi、uvicorn、pydantic-settings、sqlalchemy，按需补充。
