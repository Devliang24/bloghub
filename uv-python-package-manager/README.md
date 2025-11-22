# UV Python Package Manager

UV Python 包管理器完整教程和实战项目，包含快速入门指南、清华大学镜像源配置和 FastAPI 实战示例。

## 🚀 项目特点

- **超快的包管理**：使用 UV 替代传统的 pip，享受 10-100 倍的速度提升
- **容器化技术**：完整的 Docker 教程，从入门到实战，含流程图详解
- **国内源优化**：配置清华大学 PyPI 镜像源和 Docker 镜像源，解决国内网络访问问题
- **现代 Python 工具链**：使用 pyproject.toml 和现代 Python 开发最佳实践
- **实战导向**：UV + FastAPI + Docker 完整项目示例，可直接用于生产环境
- **响应式设计**：支持桌面和移动设备的友好界面
- **Markdown 支持**：使用 Markdown 编写文章，支持语法高亮和 TOC

## 📁 项目结构

```
uv-python-package-manager/
├── content/                 # 教程内容目录
│   └── tutorials/
│       ├── uv/
│       │   └── getting-started.md    # 完整的 UV 快速入门教程
│       └── docker/
│           └── getting-started.md    # 完整的 Docker 快速入门教程
├── docs/                    # 技术文档和报告
│   └── INSTALLATION_REPORT.md      # UV 安装验证报告
├── examples/                # 实战项目示例
│   └── fastapi-demo/
│       └── README.md              # FastAPI + UV 实战教程
├── static/                  # 静态资源
│   ├── css/
│   │   └── style.css               # 响应式 CSS 样式
│   └── js/
├── templates/               # HTML 模板
│   ├── base.html                  # 基础模板
│   ├── index.html                 # 首页模板
│   └── article.html               # 文章模板
├── scripts/                 # Python 脚本
│   └── generate_blog.py           # 静态博客生成器
├── public/                  # 生成的静态网站
│   ├── index.html                 # 博客首页
│   ├── static/                    # 复制的静态资源
│   └── tutorials/                 # 生成的教程页面
├── pyproject.toml          # 项目配置和依赖管理（UV 配置）
├── uv.lock                 # UV 依赖锁定文件
└── README.md              # 本项目说明文档
```

## 🛠️ 环境要求

- Python 3.8+
- UV 包管理器
- Git

## 📦 安装和设置

### 1. 安装 UV

```bash
# 使用 pip 安装（推荐）
pip install uv

# 或者使用官方脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 配置清华大学镜像源

```bash
# 创建配置目录
mkdir -p ~/.config/uv

# 配置清华镜像源
echo 'index-url = "https://pypi.tuna.tsinghua.edu.cn/simple/"' > ~/.config/uv/uv.toml
```

### 3. 安装依赖

```bash
# 如果是克隆的仓库，确保在当前目录
# 使用 UV 安装依赖
uv sync
```

## 🚀 快速开始

### 1. 创建模板文件

```bash
uv run python scripts/generate_blog.py --create-templates
```

### 2. 生成博客

```bash
uv run python scripts/generate_blog.py
```

### 3. 启动本地服务器

```bash
cd public
python -m http.server 8000
```

然后访问 `http://localhost:8000` 查看博客。

## 📝 编写文章

1. 在 `content/` 目录下创建 Markdown 文件
2. 使用标准的 Markdown 格式编写内容
3. 可以在文件开头添加 YAML 前置元数据：

```markdown
---
title: "文章标题"
description: "文章描述"
date: "2025-01-15"
author: "作者名"
tags: ["标签1", "标签2"]
category: "分类"
---

# 文章内容

这里是文章的正文内容...
```

## 🛠️ 开发

### 添加新依赖

```bash
# 添加生产依赖
uv add package_name

# 添加开发依赖
uv add --dev pytest black flake8
```

### 代码格式化

```bash
# 格式化代码
uv run black .

# 检查代码质量
uv run flake8 scripts/

# 类型检查
uv run mypy scripts/
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=scripts --cov-report=html
```

## 📚 主要功能

### 博客生成器 (`scripts/generate_blog.py`)

- ✅ 解析 Markdown 文件
- ✅ 支持前置元数据
- ✅ 生成 HTML 页面
- ✅ 响应式模板
- ✅ 静态文件管理
- ✅ 目录索引生成

### UV 教程内容 (`content/tutorials/uv/getting-started.md`)

- ✅ UV 安装指南（多种安装方法）
- ✅ 清华大学镜像源配置（全局、项目级）
- ✅ FastAPI 实战示例（完整项目演示）
- ✅ 常用命令速查表（项目管理、包管理）
- ✅ 问题解决方案（网络、依赖、环境问题）

### Docker 教程内容 (`content/tutorials/docker/getting-started.md`)

- ✅ Docker 核心概念和架构（含 Mermaid 流程图）
- ✅ Ubuntu 22.04 安装指南（多种安装方式）
- ✅ 国内镜像源配置（网易、DaoCloud 等）
- ✅ 镜像和容器管理（完整命令速查表）
- ✅ Dockerfile 编写和多阶段构建
- ✅ Docker Compose 多容器编排
- ✅ Python/FastAPI 应用容器化实战
- ✅ UV + FastAPI + MySQL 完整示例
- ✅ 常见问题排查和最佳实践

### 技术文档 (`docs/`)

- ✅ UV 安装验证报告（基于实际系统测试）
- ✅ 性能对比分析（UV vs pip）
- ✅ 配置最佳实践

### 实战示例 (`examples/`)

- ✅ FastAPI + UV 完整项目示例
- ✅ 部署和运维指南
- ✅ Docker 容器化示例

## 🎨 自定义

### 修改样式

编辑 `static/css/style.css` 文件来自定义博客的外观。

### 修改模板

在 `templates/` 目录下修改 HTML 模板文件：

- `base.html`: 基础模板
- `index.html`: 首页模板
- `article.html`: 文章模板

## 🚀 部署

### GitHub Pages

1. 将代码推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择 `uv-python-package-manager/public` 目录作为源

### 手动部署

```bash
# 生成博客
uv run python scripts/generate_blog.py

# 上传 public 目录到服务器
rsync -av public/ user@server:/var/www/html/
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

### Python 包管理
- [UV 官方文档](https://docs.astral.sh/uv/)
- [UV GitHub 仓库](https://github.com/astral-sh/uv)
- [清华大学 PyPI 镜像](https://pypi.tuna.tsinghua.edu.cn/)

### 容器化技术
- [Docker 官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)

### Web 框架
- [FastAPI 文档](https://fastapi.tiangolo.com/)

## 🙏 致谢

- [Astral](https://astral.sh/) - 创建了优秀的 UV 包管理器
- [FastAPI](https://fastapi.tiangolo.com/) - 现代的 Python Web 框架
- [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/) - 提供快速的 PyPI 镜像服务

---

> 💡 **小贴士**：如果你在使用过程中遇到问题，可以查看 [UV 官方文档](https://docs.astral.sh/uv/) 或提交 Issue。