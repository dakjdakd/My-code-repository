from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import asyncio
from typing import Dict
import json
import base64
from test2_gradio import WebSocketClient, send_audio_data, handle_received_message
import wave
import io
import traceback
import numpy as np
from scipy import signal
import time
import os

# http://localhost:8000

# 确保 static 目录存在
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置静态文件和模板 - 使用绝对路径
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 存储WebSocket连接和前端WebSocket连接
websocket_connections: Dict[str, tuple[WebSocketClient, asyncio.Queue]] = {}
frontend_websockets: Dict[str, WebSocket] = {}

def apply_fade(audio_data, sample_rate=24000, fade_duration=0.005):
    """对音频应用淡入淡出效果"""
    return audio_data  # 直接返回原始数据，跳过处理

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/connect")
async def connect(data: dict):
    api_key = data.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")

    message_queue = asyncio.Queue()
    uri = "wss://open.bigmodel.cn/api/paas/ws/chat"
    headers = {"authorization": api_key}
    
    ws_client = WebSocketClient(uri, headers, message_queue)
    success, message = await ws_client.connect()
    
    if success:
        websocket_connections[api_key] = (ws_client, message_queue)
        return {"success": True, "message": message}
    else:
        return {"success": False, "message": message}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket连接已接受")
    
    try:
        data = await websocket.receive_json()
        api_key = data.get("api_key")
        print(f"收到API key: {api_key[:10]}...")
        
        if not api_key or api_key not in websocket_connections:
            print("无效的API key")
            await websocket.close(code=1008, reason="Invalid API key")
            return
            
        frontend_websockets[api_key] = websocket
        ws_client, message_queue = websocket_connections[api_key]
        
        audio_chunks = []
        
        while True:
            try:
                print("等待消息队列...")
                message = await message_queue.get()
                if message:
                    print("从队列收到消息:", message[:200])  # 打印消息前200个字符
                    try:
                        result_json = json.loads(message)
                        
                        if "message" in result_json:
                            print("消息类型:", result_json["message"].get("type"))
                            
                            if result_json["message"]["type"] == "audio":
                                print("处理音频消息")
                                audio_chunk = await handle_received_message(message)
                                if audio_chunk:
                                    print(f"收到音频块，大小: {len(audio_chunk)} bytes")
                                    audio_chunks.append(audio_chunk)
                            
                            elif result_json["message"]["type"] == "event":
                                print("事件类型:", result_json["message"].get("content"))
                                if result_json["message"]["content"] == "finish":
                                    print("对话结束，准备发送完整音频")
                                    if audio_chunks:
                                        # ... 处理音频发送 ...
                                        print("开始处理音频发送")
                                        combined_audio = b''.join(audio_chunks)
                                        print(f"合并后音频大小: {len(combined_audio)} bytes")
                                        
                                        wav_buffer = io.BytesIO()
                                        with wave.open(wav_buffer, 'wb') as wav_file:
                                            wav_file.setnchannels(1)
                                            wav_file.setsampwidth(2)
                                            wav_file.setframerate(24000)
                                            wav_file.writeframes(combined_audio)
                                        
                                        wav_data = wav_buffer.getvalue()
                                        audio_base64 = base64.b64encode(wav_data).decode('utf-8')
                                        
                                        print("准备发送到前端")
                                        await websocket.send_json({
                                            "type": "audio",
                                            "audio": audio_base64
                                        })
                                        print("音频发送完成")
                                        audio_chunks = []
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {str(e)}")
                        continue
            except Exception as e:
                print(f"处理消息时出错: {str(e)}")
                traceback.print_exc()
    except Exception as e:
        print(f"WebSocket错误: {str(e)}")
        traceback.print_exc()
    finally:
        if api_key in frontend_websockets:
            del frontend_websockets[api_key]
        await websocket.close()

@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...), api_key: str = None):
    start_time = time.time()
    print(f"开始处理音频上传请求: {time.time()}")
    
    if not api_key or api_key not in websocket_connections:
        raise HTTPException(status_code=400, detail="Invalid API key")
        
    try:
        # 保存上传的音频文件
        temp_file = Path("temp_audio.wav")
        with temp_file.open("wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        print(f"音频文件保存完成，耗时: {time.time() - start_time:.2f}秒")
        
        # 获取WebSocket客户端
        ws_client, _ = websocket_connections[api_key]
        
        # 发送音频数据到AI服务
        await send_audio_data(ws_client, str(temp_file))
        
        print(f"音频数据发送完成，总耗时: {time.time() - start_time:.2f}秒")
        
        # 删除临时文件
        temp_file.unlink()
        
        return JSONResponse({"success": True})
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 