---
title: "FastAPI 教程 - 12. JWT 认证实战"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "JWT", "Authentication", "Token"]
author: "Devliang24"
description: "完整的 JWT 登录实现：用户验证、Token 生成、Token 解析以及受保护路由的访问控制。"
---

# FastAPI 教程 - 12. JWT 认证实战

> **适合人群**：后端开发者
> **前置知识**：OAuth2 基础, Python cryptography
> **预计时间**：30 分钟

## 🛠️ 准备工作

我们需要安装 `python-jose`（用于处理 JWT）和 `passlib`（用于密码哈希）。

```bash
uv add "python-jose[cryptography]" "passlib[bcrypt]"
```

## 📝 完整实现代码

这是一个简化的完整示例，包含：
1.  用户模型
2.  密码验证
3.  JWT 生成
4.  登录接口
5.  受保护接口

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# --- 配置 ---
SECRET_KEY = "your-super-secret-key" # 生产环境请从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 工具初始化 ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# --- 数据模型 ---
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

# --- 模拟数据库 ---
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password_hash": pwd_context.hash("secret"), # 存储哈希后的密码
    }
}

# --- 辅助函数 ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(username=user["username"])

# --- 路由 ---

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not pwd_context.verify(form_data.password, user_dict["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
```

## 🔍 核心逻辑解析

1.  **`/token` 接口**：
    *   接收 `OAuth2PasswordRequestForm`（表单数据，包含 username/password）。
    *   验证用户名和密码。
    *   如果通过，使用 `python-jose` 生成 JWT Token 并返回。
2.  **`get_current_user` 依赖**：
    *   依赖于 `oauth2_scheme` 拿到 Token。
    *   解析 Token，取出 username。
    *   如果在数据库找不到用户或 Token 无效，抛出 401 错误。
    *   如果成功，返回 User 对象。
3.  **受保护路由 `/users/me/`**：
    *   依赖 `get_current_user`。
    *   这意味着：**只有携带有效 Token 的请求才能进入此函数**。

## 🚀 测试

1.  打开 `/docs`。
2.  点击 **Authorize**。
3.  用户名: `johndoe`，密码: `secret`。
4.  点击 Login。Swagger UI 会自动保存 Token。
5.  现在尝试调用 `/users/me/`，你会看到成功的响应。
6.  点击 Logout 后再次调用，会看到 401 Unauthorized。

## 📚 总结

*   使用 `passlib` 处理密码哈希。
*   使用 `python-jose` 生成和解析 JWT。
*   创建一个 `get_current_user` 依赖项，在其中完成所有的 Token 验证逻辑。
*   在路由中注入 User 对象，既实现了安全保护，又方便了业务逻辑。

下一章，我们将学习如何连接真实的数据库：**SQLModel**。
