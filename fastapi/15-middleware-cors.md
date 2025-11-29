---
title: "FastAPI 教程 - 15. 中间件与 CORS"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "Middleware", "CORS", "跨域"]
author: "Devliang24"
description: "了解如何编写中间件来拦截和处理请求，以及如何配置 CORS 以允许前端跨域访问 API。"
---

# FastAPI 教程 - 15. 中间件与 CORS

> **适合人群**：Web 全栈开发者
> **前置知识**：HTTP 协议
> **预计时间**：15 分钟

## 🛡️ 什么是中间件？

**中间件 (Middleware)** 是一个函数，它在：
1.  每个**请求**被路由处理函数处理**之前**运行。
2.  每个**响应**返回之前运行。

你可以利用它来记录日志、计算处理时间、添加特定的 Header 等。

## ⏱️ 编写一个计时中间件

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 1. 请求处理前
    start_time = time.time()
    
    # 2. 调用对应的路径操作处理请求
    response = await call_next(request)
    
    # 3. 请求处理后
    process_time = time.time() - start_time
    
    # 4. 添加自定义 Header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

当你访问这个 API 时，查看浏览器的 Network 面板或使用 curl，你会发现响应头多了一个 `X-Process-Time`。

## 🌐 跨域资源共享 (CORS)

如果你的前端运行在 `http://localhost:3000`（如 React/Vue），而后端运行在 `http://localhost:8000`，浏览器默认会拦截跨域请求。

你需要配置 **CORS (Cross-Origin Resource Sharing)**。

FastAPI 提供了内置的 `CORSMiddleware`。

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000", # 允许前端开发服务器
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 允许的源列表
    allow_credentials=True,     # 是否允许携带 Cookie 等凭证
    allow_methods=["*"],        # 允许的 HTTP 方法 (GET, POST...)
    allow_headers=["*"],        # 允许的 HTTP Header
)
```

⚠️ **注意**：虽然可以将 `allow_origins` 设置为 `["*"]` 允许所有，但在生产环境中建议明确指定域名以提高安全性。

## 📚 总结

*   使用 `@app.middleware("http")` 定义自定义中间件。
*   使用 `CORSMiddleware` 解决跨域问题。
*   中间件可以拦截请求和响应，是处理全局逻辑（如日志、鉴权、Header）的好地方。

下一章，我们将学习如何处理**后台任务**，让 API 响应更快。
