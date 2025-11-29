---
title: "FastAPI 教程 - 14. CRUD 操作"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "SQLModel", "CRUD"]
author: "Devliang24"
description: "使用 SQLModel 和 FastAPI 实现完整的创建(Create)、读取(Read)、更新(Update)和删除(Delete)操作。"
---

# FastAPI 教程 - 14. CRUD 操作

> **适合人群**：后端开发者
> **前置知识**：SQLModel 连接配置
> **预计时间**：25 分钟

本章基于上一章的 `Hero` 模型和 `get_session` 依赖。

## ➕ 创建 (Create)

```python
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)  # 刷新以获取生成的 ID
    return hero
```

FastAPI 自动将请求 JSON 转换为 `Hero` 对象，SQLModel 将其保存到数据库。

## 🔍 读取 (Read)

### 读取列表

```python
from sqlmodel import select

@app.get("/heroes/", response_model=list[Hero])
def read_heroes(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement).all()
    return heroes
```

### 读取单个

```python
from fastapi import HTTPException

@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

## ✏️ 更新 (Update)

更新通常需要处理部分字段更新。我们通常会定义一个单独的 Update 模型（所有字段可选）。

```python
# 定义 Update 模型（所有字段可选）
class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

@app.patch("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_data: HeroUpdate, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # 只更新客户端传过来的字段
    hero_data_dict = hero_data.model_dump(exclude_unset=True)
    for key, value in hero_data_dict.items():
        setattr(db_hero, key, value)
        
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

*   `exclude_unset=True`：非常关键，只获取客户端实际发送的数据，避免将未发送的字段误更新为 `None`。

## ❌ 删除 (Delete)

```python
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

## 📚 总结

*   使用 `session.add` 创建。
*   使用 `session.exec(select(...))` 查询列表。
*   使用 `session.get` 查询单个。
*   使用 `exclude_unset=True` 处理部分更新。
*   使用 `session.delete` 删除。

下一章，我们将学习如何处理**中间件和跨域问题**。
