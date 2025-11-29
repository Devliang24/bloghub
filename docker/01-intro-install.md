---
title: "Docker 教程 - 01. 简介与安装"
date: "2025-11-30"
category: "Docker"
tags: ["Docker", "容器化", "安装", "镜像源"]
author: "Devliang24"
description: "了解 Docker 的核心架构，在 Windows/Linux 上安装 Docker，并配置国内镜像加速器以提升下载速度。"
---

# Docker 教程 - 01. 简介与安装

> **适合人群**：所有开发者
> **前置知识**：操作系统基础
> **预计时间**：15 分钟

## 🐳 什么是 Docker？

Docker 是一个开源的应用容器引擎。它允许开发者将应用及其依赖打包到一个可移植的**容器**中，然后发布到任何流行的 Linux 机器或 Windows 机器上。

### 核心架构

```mermaid
graph LR
    Client[Docker Client<br>(CLI)] -- 命令 --> Daemon[Docker Daemon<br>(Server)]
    Daemon -- 拉取 --> Registry[Docker Registry<br>(Docker Hub)]
    Daemon -- 运行 --> Container[Containers]
    Daemon -- 管理 --> Image[Images]

    style Client fill:#f9f,stroke:#333,stroke-width:2px
    style Daemon fill:#bbf,stroke:#333,stroke-width:2px
    style Registry fill:#dfd,stroke:#333,stroke-width:2px
```

*   **镜像 (Image)**：只读模板，包含运行应用所需的所有环境和代码（类比：安装包光盘）。
*   **容器 (Container)**：镜像的运行实例（类比：安装好正在运行的软件）。
*   **仓库 (Registry)**：存放镜像的地方（类比：应用商店）。

## 🛠️ 安装 Docker

### Windows

1.  **前提**：启用 Hyper-V 或安装 WSL 2（推荐）。
2.  **下载**：访问 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)。
3.  **安装**：双击安装包，一路 Next。
4.  **启动**：安装完成后，启动 Docker Desktop。

### Linux (Ubuntu)

```bash
# 1. 移除旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 2. 更新索引
sudo apt-get update

# 3. 安装依赖
sudo apt-get install ca-certificates curl gnupg

# 4. 添加官方 GPG Key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 5. 添加仓库
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 6. 安装 Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 🚀 配置国内镜像加速 (重点)

由于网络原因，直接从 Docker Hub 拉取镜像非常慢。配置国内加速器是必须步骤。

### Windows (Docker Desktop)

1.  点击右上角齿轮图标 **Settings**。
2.  选择 **Docker Engine**。
3.  在 JSON 编辑框中添加 `registry-mirrors` 配置：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://docker.m.daocloud.io",
    "https://docker.juhe.lz.bc.googleusercontent.com",
    "https://dockerproxy.com"
  ]
}
```

4.  点击 **Apply & restart**。

### Linux

修改 `/etc/docker/daemon.json` 文件（不存在则创建）：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

> ⚠️ **注意**：镜像源地址可能会随时间失效，建议关注最新的可用镜像源列表。

## ✅ 验证安装

在终端运行：

```bash
docker run hello-world
```

如果看到 `Hello from Docker!` 的欢迎信息，说明安装和配置成功！🎉

## 📚 总结

*   Docker 架构包含客户端、服务端和仓库。
*   国内使用 Docker **必须配置镜像加速器**。
*   Windows 使用 Docker Desktop，Linux 使用 Docker Engine。

下一章，我们将学习 Docker 的**常用命令**。
