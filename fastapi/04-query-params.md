---
title: "FastAPI 教程 - 04. 查询参数"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "查询参数", "默认值", "可选参数"]
author: "Devliang24"
description: "学习如何声明查询参数，设置默认值，标记为可选，以及布尔类型的自动转换。"
---

# FastAPI 教程 - 04. 查询参数

> **适合人群**：Python 初学者
> **前置知识**：URL 结构 (?key=value)
> **预计时间**：15 分钟

## 🔍 什么是查询参数？

声明不属于路径参数的其他函数参数时，它们会自动被解释为**查询参数**。

查询参数是 URL 中 `?` 之后的部分，以 `&` 分隔，例如：
`http://127.0.0.1:8000/items/?skip=0&limit=10`

```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

在这个例子中：
*   `skip` 默认值为 `0`
*   `limit` 默认值为 `10`
*   因为有默认值，所以它们是**可选的**。

## 🔧 默认值与可选参数

你可以根据需要设置默认值：

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

*   `q` 的类型是 `str | None`（字符串或空）。
*   默认值是 `None`。
*   访问 `/items/foo?q=bar` ➜ `{"item_id": "foo", "q": "bar"}`
*   访问 `/items/foo` ➜ `{"item_id": "foo"}`

## ✅ 布尔类型转换

FastAPI 能够智能地转换布尔类型。

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, short: bool = False):
    item = {"item_id": item_id}
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

如果你访问：
*   `/items/foo?short=1`
*   `/items/foo?short=True`
*   `/items/foo?short=true`
*   `/items/foo?short=on`
*   `/items/foo?short=yes`

FastAPI 都会将 `short` 解析为 Python 的 `True`！

## 📚 总结

*   函数参数（非路径参数）自动解析为查询参数。
*   提供默认值即可使参数变为可选。
*   `bool` 类型支持多种 URL 表达方式（1, true, yes, on）。

下一章，我们将学习如何接收更复杂的数据：**请求体**。
