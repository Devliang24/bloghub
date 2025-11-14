# FastAPI + UV 实战示例

这是一个使用 UV Python 包管理器创建的 FastAPI 项目示例，展示如何在实际项目中使用 UV。

## 🚀 项目特点

- 使用 UV 进行包管理和虚拟环境管理
- 配置清华大学镜像源加速包安装
- 现代化的 FastAPI Web 应用
- 包含完整的 CRUD 操作示例
- 支持自动 API 文档生成

## 📁 项目结构

```
fastapi-demo/
├── main.py                 # FastAPI 应用主文件
├── models.py              # 数据模型定义
├── database.py            # 数据库连接配置
├── crud.py                # CRUD 操作
├── schemas.py             # Pydantic 模式
├── requirements.txt       # 传统依赖文件（可选）
├── pyproject.toml         # UV 项目配置
└── README.md              # 项目说明
```

## 🛠️ 环境要求

- Python 3.8+
- UV 包管理器
- SQLite3（默认）

## 📦 快速开始

### 1. 安装 UV（如果还未安装）

```bash
pip install uv
```

### 2. 配置清华大学镜像源

```bash
# 配置全局镜像源
mkdir -p ~/.config/uv
echo 'index-url = "https://pypi.tuna.tsinghua.edu.cn/simple/"' > ~/.config/uv/uv.toml
```

### 3. 创建项目

```bash
# 创建新项目
uv init fastapi-demo
cd fastapi-demo

# 配置项目使用清华源
echo 'index-url = "https://pypi.tuna.tsinghua.edu.cn/simple/"' > uv.toml
```

### 4. 安装依赖

```bash
# 安装 FastAPI 和相关依赖
uv add fastapi uvicorn[standard]

# 安装数据库和其他依赖
uv add sqlalchemy pydantic-settings python-multipart

# 开发依赖
uv add --dev pytest pytest-asyncio httpx
```

### 5. 创建应用文件

创建 `main.py` 文件：

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from .database import SessionLocal, engine, Base
from . import models, schemas, crud

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI + UV 示例",
    description="使用 UV 构建的 FastAPI 应用",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "message": "欢迎使用 FastAPI + UV",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 用户 CRUD 操作
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

# 文章 CRUD 操作
@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db=db, article=article)

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles

@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return db_article

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6. 运行应用

```bash
# 启动开发服务器
uv run uvicorn main:app --reload

# 或者生产模式
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API 文档

启动应用后，可以访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 测试

```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=app --cov-report=html
```

## 🔧 开发工具

### 代码格式化

```bash
# 格式化代码
uv run black .

# 检查代码质量
uv run flake8 .
```

### 类型检查

```bash
# 类型检查
uv run mypy .
```

## 📦 依赖管理

### 添加新依赖

```bash
# 添加生产依赖
uv add package_name

# 添加特定版本
uv add "package_name>=1.0,<2.0"

# 添加开发依赖
uv add --dev pytest
```

### 查看和更新依赖

```bash
# 查看已安装的包
uv pip list

# 更新包到最新版本
uv add package_name@latest

# 同步环境到 pyproject.toml
uv sync
```

### 导出传统 requirements.txt

```bash
# 生成 requirements.txt
uv pip freeze > requirements.txt
```

## 🚀 部署

### 构建 Docker 镜像

```dockerfile
FROM python:3.10-slim

# 安装 UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY . .

# 安装依赖
RUN uv sync --frozen

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 使用 systemd 服务

创建 `/etc/systemd/system/fastapi-demo.service`:

```ini
[Unit]
Description=FastAPI Demo
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/path/to/fastapi-demo
Environment=PATH=/path/to/fastapi-demo/.venv/bin
ExecStart=/path/to/fastapi-demo/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用并启动服务
sudo systemctl enable fastapi-demo
sudo systemctl start fastapi-demo
```

## 🔗 相关链接

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [UV 官方文档](https://docs.astral.sh/uv/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License