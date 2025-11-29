
# FastAPI 教程 - 17. 自动化测试

> **适合人群**：所有开发者
> **前置知识**：Pytest 基础（可选）
> **预计时间**：20 分钟

## 🧪 为什么要测试？

自动化测试可以让你在修改代码后，确信没有破坏原有的功能。FastAPI 基于 Starlette，因此使用 `TestClient` 进行测试非常简单且直观。

## 🛠️ 安装测试工具

你需要安装 `pytest` 和 `httpx`。

```bash
uv add --dev pytest httpx
```

## 📝 编写测试

假设我们有文件 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

创建一个文件 `test_main.py`：

```python
from fastapi.testclient import TestClient
from main import app

# 创建测试客户端
client = TestClient(app)

def test_read_main():
    # 发送请求
    response = client.get("/")
    
    # 断言状态码
    assert response.status_code == 200
    
    # 断言响应内容
    assert response.json() == {"msg": "Hello World"}
```

## 🏃‍♂️ 运行测试

在命令行运行：

```bash
uv run pytest
```

输出示例：
```
test_main.py .                                                          [100%]

============================== 1 passed in 0.03s ===============================
```

## 🧩 测试数据库应用

当测试涉及数据库时，通常的最佳实践是：
1.  创建一个临时的 SQLite 数据库（或使用 `sqlite:///:memory:`）。
2.  使用 `dependency_overrides` 覆盖原本的数据库会话依赖。

```python
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session, Hero

# 1. 创建内存数据库
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
SQLModel.metadata.create_all(engine)

# 2. 覆盖依赖项
def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def test_create_hero():
    response = client.post(
        "/heroes/",
        json={"name": "Deadpond", "secret_name": "Dive Wilson"},
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["id"] is not None
```

**`app.dependency_overrides`** 是 FastAPI 测试的神器，它可以让你在测试时轻松替换掉任何依赖项（数据库、认证、外部 API 调用等）。

## 📚 总结

*   使用 `TestClient` 发送请求并检查响应。
*   配合 `pytest` 运行测试。
*   使用 `app.dependency_overrides` 在测试中替换依赖项，隔离环境。

下一章，我们将探索实时通信：**WebSockets**。
