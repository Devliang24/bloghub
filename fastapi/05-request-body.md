
# FastAPI 教程 - 05. 请求体

> **适合人群**：Python 初学者
> **前置知识**：JSON 基础，Python 类
> **预计时间**：20 分钟

## 📦 什么是请求体？

**请求体**（Request Body）是客户端（如浏览器、API 客户端）发送给 API 的数据。而**响应体**（Response Body）是 API 发送回客户端的数据。

在 FastAPI 中，我们使用 **Pydantic** 模型来声明请求体。

## 🛠️ 定义数据模型

首先，从 `pydantic` 导入 `BaseModel`：

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 代码解析

1.  **定义模型**：创建一个继承自 `BaseModel` 的类 `Item`。
2.  **声明属性**：使用标准 Python 类型提示。
    *   `name` 和 `price` 是必填项。
    *   `description` 和 `tax` 有默认值 `None`，所以是选填项。
3.  **作为参数**：将 `item` 参数的类型声明为 `Item` 类。

## 🚀 自动处理

FastAPI 将自动执行以下操作：

1.  **读取**：将请求体作为 JSON 读取。
2.  **转换**：将类型转换为你定义的 Python 类型（例如将 JSON 的字符串数字转为 `float`）。
3.  **校验**：如果数据无效（例如 `price` 传了 "abc"），返回清晰的错误信息。
4.  **文档**：生成的 JSON Schema 将用于自动 API 文档。

## 🔧 使用数据

在函数内部，你可以直接访问模型对象的属性：

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### 在文档中查看

启动服务器并访问 `/docs`。你会发现在 `POST /items/` 接口下，FastAPI 自动生成了请求体示例：

```json
{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0
}
```

## 📚 总结

*   使用 `Pydantic` 的 `BaseModel` 定义数据结构。
*   FastAPI 自动处理 JSON 解析、数据校验和文档生成。
*   你可以像操作普通对象一样操作请求体数据。

下一章，我们将学习如何对**查询参数**进行更细致的校验。
