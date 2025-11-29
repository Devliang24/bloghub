
# FastAPI 教程 - 08. 多参数混合

> **适合人群**：Web 开发者
> **前置知识**：Path, Query, Body 基础
> **预计时间**：15 分钟

## 🤹 混合使用 Path, Query 和 Body

FastAPI 的强大之处在于它可以轻松地混合使用多种类型的参数。它会根据参数的声明方式自动区分：

*   如果在**路径**中声明了：就是**路径参数**。
*   如果是 **Pydantic 模型**：就是**请求体**。
*   如果是**单值类型**（int, str 等）且不在路径中：就是**查询参数**。

```python
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., title="The ID of the item", ge=0),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

在这个例子中，FastAPI 会准确地知道：
1.  `item_id` 来自 URL 路径 `/items/42`。
2.  `q` 来自查询字符串 `?q=search`。
3.  `item` 来自 HTTP 请求体（JSON）。

## 📦 多个请求体参数

如果你需要在一个请求中接收多个模型怎么办？比如同时接收 `Item` 和 `User` 信息。

```python
class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}
```

此时，FastAPI 会期望请求体是一个包含两个键的 JSON 对象：

```json
{
    "item": {
        "name": "Foo",
        "price": 50.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

## 🎯 嵌入式 Body 参数

如果你只有一个模型 `Item`，但你希望它在 JSON 中也是以 key 的形式存在（类似上面的结构），可以使用 `Body(embed=True)`。

```python
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    return {"item_id": item_id, "item": item}
```

此时请求体必须是：
```json
{
    "item": {
        "name": "Foo",
        "price": 50.2
    }
}
```
而不是直接就是 Item 的内容。

## 📚 总结

*   FastAPI 自动根据上下文区分参数来源。
*   可以在一个接口中任意组合 Path、Query 和 Body。
*   支持同时接收多个 Pydantic 模型。
*   使用 `Body(embed=True)` 可以强行将单模型包裹在 JSON 对象中。

下一章，我们将进入进阶主题，学习 FastAPI 强大的**依赖注入**系统。
