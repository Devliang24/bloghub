---
title: "FastAPI 教程 - 02. 第一步"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "基础", "交互式文档"]
author: "Devliang24"
description: "编写第一个 FastAPI 应用，学习如何运行开发服务器并使用自动生成的交互式文档。"
---

# FastAPI 教程 - 02. 第一步

> **适合人群**：Python 初学者
> **前置知识**：已安装 FastAPI
> **预计时间**：10 分钟

## 📝 最简单的 FastAPI 文件

让我们详细剖析上一章的 `main.py`：

```python
from fastapi import FastAPI

# 1. 创建一个 FastAPI 实例
app = FastAPI()

# 2. 定义路径操作装饰器
@app.get("/")
# 3. 定义路径操作函数
async def root():
    # 4. 返回内容
    return {"message": "Hello World"}
```

### 代码解析

1.  **导入 FastAPI**：`FastAPI` 是一个继承自 `Starlette` 的类。
2.  **创建实例**：`app` 变量是应用的核心，后续运行命令会用到它（`main:app`）。
3.  **路径操作装饰器**：
    *   `@app.get("/")` 告诉 FastAPI，当用户访问根路径 `/` 且使用 `GET` 方法时，执行下方的函数。
    *   支持的操作：`@app.post()`, `@app.put()`, `@app.delete()` 等。
4.  **路径操作函数**：如果是异步函数使用 `async def`，普通函数使用 `def` 也可以。
5.  **返回内容**：你可以返回 `dict`、`list`、`str`、`int` 等，FastAPI 会自动将其转换为 JSON 格式。

## 🚀 运行开发服务器

使用 `fastapi dev` 命令运行开发服务器：

```bash
uv run fastapi dev main.py
```

*   **`fastapi dev`**：启动开发模式，代码修改后会自动重载。
*   **`main.py`**：你的 Python 文件名。

## 📑 交互式 API 文档

这是 FastAPI 最酷的功能之一！应用启动后，访问：

👉 **http://127.0.0.1:8000/docs**

你会看到基于 **Swagger UI** 的自动交互式文档：

1.  点击 `GET /` 按钮。
2.  点击 `Try it out`。
3.  点击 `Execute`。
4.  你将看到服务器的响应结果：
    ```json
    {
      "message": "Hello World"
    }
    ```

### 备用文档 (ReDoc)

FastAPI 还提供了另一种风格的文档，访问：

👉 **http://127.0.0.1:8000/redoc**

## 📚 总结

*   使用 `@app.get("/")` 定义路由。
*   函数返回值自动转换为 JSON。
*   `fastapi dev` 启动服务器。
*   `/docs` 提供了强大的交互式文档。

下一章，我们将学习如何处理**路径参数**，让 URL 变得动态起来。
