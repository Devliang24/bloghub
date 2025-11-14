# Blog Hub

一个整合了多个技术博客和教程的项目仓库。

## 📁 项目结构

```
bloghub/
├── uv-python-package-manager/    # UV Python包管理器教程
└── ...                          # 更多项目即将添加
```

## 🚀 当前项目

### UV Python Package Manager

完整的 UV Python 包管理器学习和实战项目，包含：

- 📖 详细教程：从安装到实战的完整指南
- 🔧 配置指南：清华大学镜像源配置
- 💻 实战示例：FastAPI 项目演示
- 📊 性能对比：UV vs pip 的详细对比
- 🎯 国内优化：针对中国用户的特殊配置

#### 快速开始

```bash
# 进入 UV 项目
cd uv-python-package-manager

# 生成博客网站
uv run python scripts/generate_blog.py

# 启动本地服务器
cd public && python -m http.server 8000

# 访问 http://localhost:8000
```

## 🔗 相关链接

- **UV 项目主页**: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- **UV 官方文档**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **清华 PyPI 镜像**: [https://pypi.tuna.tsinghua.edu.cn/](https://pypi.tuna.tsinghua.edu.cn/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

> 💡 提示：各个子项目都是独立的，可以单独使用和学习。