---
title: "FastAPI 教程 - 03. 路径参数"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "路径参数", "类型转换", "Enum"]
author: "Devliang24"
description: "学习如何声明路径参数，使用 Python 类型提示进行自动解析和验证，以及如何使用枚举限制参数值。"
---

# FastAPI 教程 - 03. 路径参数

> **适合人群**：Python 初学者
> **前置知识**：Python f-string
> **预计时间**：15 分钟

## 🎯 声明路径参数

你可以使用与 Python 格式化字符串相同的语法来声明路径参数：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

访问 `http://127.0.0.1:8000/items/foo`，响应如下：

```json
{"item_id": "foo"}
```

## 🔢 有类型的路径参数

如果你想让 `item_id` 必须是整数，可以使用 Python 的标准类型提示：

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### 自动数据转换

访问 `http://127.0.0.1:8000/items/3`，响应如下：

```json
{"item_id": 3}
```

注意，响应中的 `3` 是一个数字 `int`，而不是字符串 `"3"`。FastAPI 自动为你完成了类型转换。

### 自动数据验证

如果你访问 `http://127.0.0.1:8000/items/foo`（非数字），你会得到一个清晰的错误提示：

```json
{
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

## 🚦 预定义值 (Enum)

如果你想让路径参数只能是固定的几个值之一，可以使用 Python 的 `Enum` 类。

```python
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
        
    return {"model_name": model_name, "message": "Have some residuals"}
```

在 **/docs** 文档中，这个参数将显示为一个下拉菜单，用户只能选择定义好的值。

## 📚 总结

*   使用 `{parameter}` 声明路径参数。
*   使用类型提示 `param: int` 进行自动类型转换和验证。
*   使用 `Enum` 类限制参数的可选值。

下一章，我们将学习如何处理**查询参数**。
