
# FastAPI 教程 - 06. 查询参数校验

> **适合人群**：Web 开发者
> **前置知识**：正则表达式基础（可选）
> **预计时间**：15 分钟

## 🎯 引入 Query

FastAPI 允许你为参数声明额外的信息和校验。我们需要从 `fastapi` 导入 `Query`。

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

在这里，我们将 `q` 的默认值设置为 `None`，同时使用 `Query(default=None)` 声明它是一个查询参数。

## 📏 长度限制与正则

你可以添加多种约束：

```python
q: str | None = Query(
    default=None, 
    min_length=3, 
    max_length=50, 
    pattern="^fixedquery$"
)
```

*   `min_length`: 最小长度
*   `max_length`: 最大长度
*   `pattern`: 正则表达式（例如：必须是 `fixedquery`）

如果客户端传递的参数不符合规则，FastAPI 将直接返回 422 错误，而不会执行你的函数逻辑。

## 📝 必填参数

如果你想让参数变为必填，同时还要加上校验规则，只需不设置默认值（使用 `...`）：

```python
async def read_items(q: str = Query(min_length=3)):
    ...
```

或者在 Python 3.10+ 中使用更显式的方式：

```python
async def read_items(q: str = Query(..., min_length=3)):
    ...
```

## 📋 参数列表（多个值）

你可以接收一个参数的多个值，例如 `?q=foo&q=bar`。

```python
from typing import List

@app.get("/items/")
async def read_items(q: List[str] | None = Query(default=None)):
    query_items = {"q": q}
    return query_items
```

在文档中，这将自动显示为可添加多个项目的输入框。

## 🏷️ 添加元数据

你可以添加更多信息，这些信息将展示在 API 文档中：

```python
q: str | None = Query(
    default=None,
    title="查询字符串",
    description="用于过滤项目的查询字符串，必须在3-50个字符之间",
    alias="item-query", # 允许 URL 中使用 item-query 代替 q
    deprecated=True     # 标记为已过时
)
```

## 📚 总结

*   使用 `Query` 为查询参数添加校验（长度、正则）。
*   使用 `Query(default=...)` 声明必填项。
*   支持列表参数 `List[str]`。
*   添加 `title`, `description` 等元数据丰富文档。

下一章，我们将把这些校验技巧应用到**路径参数**上。
