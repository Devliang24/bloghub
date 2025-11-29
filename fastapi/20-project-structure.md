---
title: "FastAPI 教程 - 20. 大型项目结构"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "架构", "最佳实践"]
author: "Devliang24"
description: "学习如何组织大型 FastAPI 项目的代码结构，使用 APIRouter 分解路由，实现清晰、可维护的模块化架构。"
---

# FastAPI 教程 - 20. 大型项目结构

> **适合人群**：架构师, 高级开发者
> **前置知识**：Python 模块导入
> **预计时间**：15 分钟

## 🏗️ 为什么需要规划结构？

把所有代码都写在 `main.py` 里对于 Demo 是可以的，但对于真实的生产项目，这会是一场灾难。我们需要**模块化**。

## 📂 推荐目录结构

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py           # 入口文件
│   ├── dependencies.py   # 全局依赖
│   ├── routers/          # 路由模块
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   ├── internal/         # 内部逻辑
│   │   ├── __init__.py
│   │   └── admin.py
│   └── database.py       # 数据库配置
├── tests/                # 测试用例
├── pyproject.toml
└── README.md
```

## 🛣️ 使用 APIRouter

`APIRouter` 就像是一个迷你的 `FastAPI` 应用。你可以用它来定义一组路由，然后将其注册到主应用中。

### 1. 定义路由模块 (`app/routers/users.py`)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}
```

### 2. 定义另一个模块 (`app/routers/items.py`)

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]
```

*   `prefix="/items"`：该模块下所有路由都会自动加上 `/items` 前缀。
*   `tags=["items"]`：Swagger UI 中这些接口会被归类到 "items" 标签下。

### 3. 在主应用中注册 (`app/main.py`)

```python
from fastapi import FastAPI
from .routers import users, items

app = FastAPI()

# 注册路由
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

## 🧩 结构优势

1.  **分离关注点**：用户逻辑在 `users.py`，商品逻辑在 `items.py`。
2.  **团队协作**：不同开发者可以同时修改不同文件，减少冲突。
3.  **可维护性**：代码清晰，易于查找和重构。

## 📚 总结

*   不要把所有代码塞进一个文件。
*   使用 `APIRouter` 分割功能模块。
*   使用 `app.include_router()` 聚合模块。
*   合理使用 `prefix` 和 `tags` 保持 API 结构清晰。

🎉 **恭喜！** 你已经完成了 FastAPI 的完整教程系列。现在你已经具备了构建高性能、生产级 Web API 的能力。去创造属于你的精彩应用吧！
