---
title: "Docker 教程 - 03. 编写 Dockerfile"
date: "2025-11-30"
category: "Docker"
tags: ["Docker", "Dockerfile", "构建", "镜像"]
author: "Devliang24"
description: "学习编写高效的 Dockerfile，理解镜像分层原理，以及如何构建自己的应用镜像。"
---

# Docker 教程 - 03. 编写 Dockerfile

> **适合人群**：开发者
> **前置知识**：Docker 常用命令
> **预计时间**：20 分钟

## 🏗️ 什么是 Dockerfile？

Dockerfile 是一个文本文件，包含了一系列指令，Docker 使用它来自动构建镜像。

### 镜像分层原理

```mermaid
graph BT
    L1[Base Image (Ubuntu)] --> L2[Add Python]
    L2 --> L3[Copy Code]
    L3 --> L4[Install Deps]
    L4 --> Final[Final App Image]
    
    style Final fill:#f96,stroke:#333,stroke-width:2px
```

每一条指令都会创建一个新的**层 (Layer)**。Docker 会缓存未变动的层，从而加速构建。

## 📝 常用指令详解

让我们写一个简单的 Python 应用 Dockerfile：

```dockerfile
# 1. FROM: 指定基础镜像
FROM python:3.10-slim

# 2. WORKDIR: 设置工作目录（后续命令都在此目录下执行）
WORKDIR /app

# 3. COPY: 复制文件 (宿主机 -> 容器)
# 先复制依赖文件，利用缓存
COPY requirements.txt .

# 4. RUN: 执行构建命令
# 使用清华源加速安装
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. COPY: 复制源代码
COPY . .

# 6. ENV: 设置环境变量
ENV PORT=8000

# 7. EXPOSE: 声明端口（仅作为文档说明）
EXPOSE 8000

# 8. CMD: 容器启动命令
CMD ["python", "app.py"]
```

### 关键点解析

*   **`FROM`**：必须是第一条指令。尽量使用官方镜像（如 `node`, `python`, `nginx`）。
*   **`slim` 版本**：如 `python:3.10-slim`，比完整版小很多，适合生产环境。
*   **`COPY` 顺序**：先复制依赖描述文件（package.json/requirements.txt），安装依赖，最后再复制源代码。这样每次只修改代码时，不需要重新下载依赖。
*   **`CMD` vs `ENTRYPOINT`**：`CMD` 指定默认命令，可以被 `docker run` 覆盖；`ENTRYPOINT` 指定不可覆盖的入口。

## 🔨 构建镜像

在 Dockerfile 所在目录执行：

```bash
# -t: 镜像标签 (name:tag)
# .: 上下文路径 (当前目录)
docker build -t my-python-app:v1 .
```

构建过程示例：
```
[+] Building 2.3s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => ...
 => [4/5] RUN pip install ...
 => [5/5] COPY . .
 => exporting to image
```

## 🚀 运行测试

```bash
docker run -d -p 8000:8000 my-python-app:v1
```

## 📚 最佳实践

1.  **使用 `.dockerignore`**：
    创建一个 `.dockerignore` 文件，排除不需要的文件，减小镜像体积。
    ```text
    .git
    __pycache__
    *.pyc
    node_modules
    ```
2.  **最小化层数**：虽然现在的 Docker 引擎优化了，但合并相关的 `RUN` 指令仍然是个好习惯。
3.  **使用国内源**：在 `RUN` 指令中配置 pip/npm/apk 的国内源，显著提升构建速度。

下一章，我们将学习如何使用 **Docker Compose** 编排多容器应用。
