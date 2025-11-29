---
title: "FastAPI 教程 - 10. 类作为依赖"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "依赖注入", "Class"]
author: "Devliang24"
description: "学习如何使用 Python 类作为依赖项，利用类的初始化方法来清理参数声明，使代码更加优雅。"
---

# FastAPI 教程 - 10. 类作为依赖

> **适合人群**：进阶开发者
> **前置知识**：Python 类, 依赖注入基础
> **预计时间**：10 分钟

## 🧹 简化参数声明

在上一章中，我们定义了一个函数 `common_parameters` 来接收分页参数。如果参数很多，每次都要写一遍类型提示可能会很繁琐。

我们可以使用 **类** 来替代函数。

```python
from fastapi import FastAPI, Depends

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 定义依赖类
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
```

### 妙用：简写形式

注意这一行：
`commons: CommonQueryParams = Depends(CommonQueryParams)`

FastAPI 允许一种简写方式。既然参数类型就是依赖类本身，你可以省略 `Depends` 中的参数：

```python
@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    # ... 代码同上
    return response
```

FastAPI 会自动推断出 `Depends()` 应该使用 `CommonQueryParams` 类来实例化。

## 🏗️ 原理

1.  FastAPI 看到 `Depends(CommonQueryParams)`。
2.  它会调用 `CommonQueryParams` 的 `__init__` 方法。
3.  它分析 `__init__` 的参数（`q`, `skip`, `limit`），就像分析普通函数参数一样。
4.  它从请求中提取这些参数。
5.  它创建 `CommonQueryParams` 的实例。
6.  它将实例传给 `read_items` 函数的 `commons` 参数。

这样，你在函数内部就可以享受到 IDE 的代码补全和类型检查（比如 `commons.skip`）。

## 📚 总结

*   使用类作为依赖项可以将参数和逻辑封装在一起。
*   FastAPI 会调用类的 `__init__` 方法来解析依赖。
*   使用 `commons: ClassName = Depends()` 简写形式可以让代码更简洁。

下一章，我们将开启一个新的重要主题：**安全与认证**。
