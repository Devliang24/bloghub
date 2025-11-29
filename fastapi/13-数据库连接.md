
# FastAPI 教程 - 13. 数据库连接 (SQLModel)

> **适合人群**：后端开发者
> **前置知识**：SQL 基础
> **预计时间**：15 分钟

## 💡 为什么选择 SQLModel？

**SQLModel** 是专门为 FastAPI 设计的 ORM 库。
*   它是 **Pydantic** 和 **SQLAlchemy** 的完美结合。
*   同一个类，既是 Pydantic 模型（用于数据校验和 API 文档），又是 SQLAlchemy 模型（用于数据库表映射）。
*   极大地减少了代码重复（不需要定义两套 Schema）。

## 🛠️ 安装 SQLModel

```bash
uv add sqlmodel
```

## 🏗️ 定义模型

```python
from typing import Optional
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

*   `table=True`：告诉 SQLModel 这是一个数据库表。
*   `Field(primary_key=True)`：设置主键。

## 🔌 建立连接

我们将使用 SQLite 作为示例数据库。

```python
from sqlmodel import create_engine, SQLModel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args={"check_same_thread": False} 仅用于 SQLite
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

*   `create_engine`：创建数据库引擎。
*   `SQLModel.metadata.create_all(engine)`：自动根据定义好的模型创建数据库表。

## 🧬 整合到 FastAPI

我们使用依赖注入来管理数据库会话（Session）。

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session

app = FastAPI()

# 在应用启动时创建表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 依赖项：获取 Session
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/heroes/")
def read_heroes(session: Session = Depends(get_session)):
    # 这里可以使用 session 进行数据库操作
    return []
```

### `yield` 的作用

在 `get_session` 中使用 `yield`：
1.  FastAPI 接收请求，执行 `session = Session(engine)`。
2.  执行路由函数逻辑。
3.  路由函数执行完毕后，FastAPI 会回到 `get_session` 继续执行 `yield` 之后的代码（这里是 `with` 语句块结束，自动关闭 Session）。
这确保了数据库连接总是被正确关闭。

## 📚 总结

*   SQLModel 让 Pydantic 和 SQLAlchemy 合二为一。
*   使用 `table=True` 定义数据表。
*   使用 `engine` 管理连接。
*   使用带有 `yield` 的依赖注入来管理 Session 的生命周期。

下一章，我们将基于此环境实现完整的 **CRUD 操作**。
