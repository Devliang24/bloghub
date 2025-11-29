---
title: "FastAPI 教程 - 18. WebSockets"
date: "2025-11-30"
category: "FastAPI"
tags: ["FastAPI", "WebSockets", "实时通信"]
author: "Devliang24"
description: "学习如何使用 FastAPI 构建 WebSocket 服务，实现客户端和服务器之间的全双工实时通信。"
---

# FastAPI 教程 - 18. WebSockets

> **适合人群**：进阶开发者
> **前置知识**：WebSocket 概念
> **预计时间**：15 分钟

## 📞 什么是 WebSocket？

传统的 HTTP 请求是单向的：客户端请求 -> 服务器响应。
**WebSocket** 建立了持久的双向连接，服务器可以随时向客户端推送消息，客户端也可以随时发送消息。常用于聊天室、实时大屏、在线游戏等。

## 🔌 编写 WebSocket 服务

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # 1. 接受连接
    await websocket.accept()
    try:
        while True:
            # 2. 接收消息 (文本)
            data = await websocket.receive_text()
            
            # 3. 发送消息
            await websocket.send_text(f"Message text was: {data}")
            await websocket.send_text(f"Client ID: {client_id}")
    except WebSocketDisconnect:
        print(f"Client #{client_id} left")
```

### 代码解析

1.  `@app.websocket("/ws")`：定义 WebSocket 路由。
2.  `await websocket.accept()`：完成握手，建立连接。
3.  `while True`：保持循环以持续监听消息。
4.  `await websocket.receive_text()`：暂停并等待客户端发送消息。
5.  `await websocket.send_text()`：向客户端发送消息。

## 🖥️ 客户端测试 (HTML)

你可以创建一个简单的 HTML 文件来测试：

```html
<!DOCTYPE html>
<html>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/123");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
```

## 📡 连接管理器

在实际应用（如聊天室）中，你通常需要管理多个连接，比如广播消息给所有在线用户。

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/chat/")
async def chat_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Someone said: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A user left the chat")
```

## 📚 总结

*   使用 `@app.websocket` 定义路由。
*   `await websocket.accept()` 接受连接。
*   `receive_text` 和 `send_text` 进行收发。
*   需要自己维护连接列表来实现广播功能。

下一章，我们将学习如何**部署**你的 FastAPI 应用。
