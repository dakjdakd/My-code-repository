import gradio as gr
import asyncio
import websockets
import time
import json
import base64
from pydub import AudioSegment
import io
import wave
import numpy as np
from scipy import signal


class WebSocketClient:
    def __init__(self, uri, headers, message_queue):
        self.uri = uri
        self.headers = headers
        self.connection = None
        self.receive_task = None
        self.message_queue = message_queue
        self.system_prompt = None
        self.should_reconnect = True
        self.max_retries = 3

    async def connect(self, retry_count=0):
        try:
            self.connection = await websockets.connect(self.uri, extra_headers=self.headers)
            print("WebSocket 连接成功")
            response = await self.connection.recv()
            print(f"服务器响应: {response}")
            self.receive_task = asyncio.create_task(self.receive_loop())
            return True, "WebSocket 连接成功"
        except Exception as e:
            print(f"连接失败：{str(e)}")
            if retry_count < self.max_retries:
                print(f"尝试重新连接 ({retry_count + 1}/{self.max_retries})")
                await asyncio.sleep(1)
                return await self.connect(retry_count + 1)
            return False, f"连接失败：{str(e)}"

    async def send(self, message):
        try:
            if not self.connection or self.connection.closed:
                print("连接已关闭，尝试重新连接")
                success, _ = await self.connect()
                if not success:
                    raise Exception("重新连接失败")
            
            print("发送消息:", message[:100] + "...")
            await self.connection.send(message)
        except Exception as e:
            print(f"发送失败：{str(e)}")
            raise

    async def receive_loop(self):
        while self.should_reconnect:
            try:
                while True:
                    if self.connection and not self.connection.closed:
                        message = await self.connection.recv()
                        print("接收到原始消息:", message[:200])
                        
                        # 检查是否是超时错误
                        try:
                            msg_data = json.loads(message)
                            if "error" in msg_data and msg_data["error"].get("code") == "3001":
                                print("检测到会话超时，尝试重新连接")
                                await self.reconnect()
                                continue
                        except:
                            pass
                            
                        await self.message_queue.put(message)
                    else:
                        print("连接已关闭，等待重新连接")
                        break
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket连接已关闭，尝试重新连接")
                await self.reconnect()
            except Exception as e:
                print(f"接收循环出错：{str(e)}")
                await asyncio.sleep(1)

    async def reconnect(self):
        print("开始重新连接...")
        if self.connection:
            await self.connection.close()
        success, _ = await self.connect()
        if success:
            print("重新连接成功")
        else:
            print("重新连接失败")

    async def close(self):
        self.should_reconnect = False
        if self.connection:
            await self.connection.close()
            print("WebSocket 连接已关闭")
        if self.receive_task:
            self.receive_task.cancel()


def reencode_audio(audio_file_path):
    try:
        audio = AudioSegment.from_file(audio_file_path)
        audio = audio.set_frame_rate(48000).set_channels(1).set_sample_width(2)
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        buffer.seek(0)
        return buffer.read(), None
    except Exception as e:
        return None, f"音频重新编码失败：{str(e)}"


def encode_audio_to_base64(audio_bytes):
    try:
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return audio_base64, None
    except Exception as e:
        return None, f"音频编码失败：{str(e)}"


def base64_to_wav(base64_string, channels=1, sample_rate=44100):
    pcm_data = base64.b64decode(base64_string)

    def pcm_to_wav_bytes(pcm_data, channels=1, sample_width=2, frame_rate=44100):
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(frame_rate)
            wf.writeframes(pcm_data)
        wav_io.seek(0)
        return wav_io.read()

    wav_bytes = pcm_to_wav_bytes(pcm_data, channels=channels, sample_width=2, frame_rate=sample_rate)
    return wav_bytes


def apply_fade(audio_data, sample_rate=24000, fade_duration=0.3):
    """使用更平滑的音频处理方法"""
    try:
        # 将字节数据转换为numpy数组
        audio_array = np.frombuffer(audio_data, dtype=np.int16).copy()
        
        # 计算淡入淡出的样本数
        fade_length = int(fade_duration * sample_rate)
        
        # 使用余弦窗口（提供更平滑的过渡）
        fade_in = np.cos(np.linspace(np.pi, 2*np.pi, fade_length)) * 0.5 + 0.5
        fade_out = np.cos(np.linspace(0, np.pi, fade_length)) * 0.5 + 0.5
        
        # 添加较长的静音段
        silence_duration = 0.3  # 300ms静音
        silence_samples = int(silence_duration * sample_rate)
        silence = np.zeros(silence_samples, dtype=np.int16)
        
        # 应用淡入淡出
        audio_array[:fade_length] = audio_array[:fade_length] * fade_in
        audio_array[-fade_length:] = audio_array[-fade_length:] * fade_out
        
        # 平滑处理
        window_size = 1024
        overlap = 512
        window = np.hanning(window_size)
        
        # 使用重叠添加方法进行平滑处理
        smoothed = np.zeros(len(audio_array))
        for i in range(0, len(audio_array) - window_size, overlap):
            smoothed[i:i+window_size] += audio_array[i:i+window_size] * window
        
        # 归一化
        smoothed = smoothed / np.max(np.abs(smoothed)) * 32767
        smoothed = smoothed.astype(np.int16)
        
        # 添加静音段，使用渐变过渡
        transition_length = int(0.05 * sample_rate)  # 50ms过渡
        transition = np.linspace(0, 1, transition_length)
        
        # 构建最终音频
        final_audio = np.concatenate([
            silence,
            smoothed * transition[:transition_length],  # 开始过渡
            smoothed[transition_length:-transition_length],  # 主要内容
            smoothed[-transition_length:] * transition[::-1],  # 结束过渡
            silence
        ])
        
        return final_audio.astype(np.int16).tobytes()
    except Exception as e:
        print(f"音频处理失败: {str(e)}")
        return audio_data


async def handle_received_message(message):
    try:
        result_json = json.loads(message)

        if "message" in result_json:
            message = result_json["message"]
            if message["type"] == "audio":
                audio_chunk = base64_to_wav(message["content"], channels=1, sample_rate=24000)
                # 添加淡入淡出效果
                audio_chunk = apply_fade(audio_chunk, sample_rate=24000, fade_duration=0.15)
                print(f"Received audio chunk, length: {len(audio_chunk)} bytes")
                return audio_chunk

            elif message["type"] == "event" and message["content"] == "finish":
                print("对话结束")
                return None
    except Exception as e:
        print(f"处理消息失败：{str(e)}")
        return None


async def connect_and_receive(api_key, message_queue):
    uri = "wss://open.bigmodel.cn/api/paas/ws/chat"
    headers = {"authorization": api_key}

    ws_client = WebSocketClient(uri, headers, message_queue)
    success, message = await ws_client.connect()
    if not success:
        print("Received")
        return None

    return ws_client


async def audio_stream(message_queue):
    while True:
        message = await message_queue.get()
        if message is None:
            break

        audio_chunk = await handle_received_message(message)
        if audio_chunk:
            yield audio_chunk


async def send_audio_data(ws_client, audio_file_path, max_retries=3):
    print(f"准备发送音频文件: {audio_file_path}")
    for retry in range(max_retries):
        try:
            audio_bytes, error = reencode_audio(audio_file_path)
            if error:
                print(error)
                return
            audio_base64, error = encode_audio_to_base64(audio_bytes)
            if error:
                print(error)
                return

            message = {
                "client_timestamp": time.time(),
                "system_prompt": ws_client.system_prompt or "你是一个AI推荐官，请根据用户的问题给出专业的推荐。",
                "chunk_type": "append",
                "audio_chunk": audio_base64,
                "control": {
                    "response_type": "audio",
                    "vad_config": {
                        "server_vad": True,
                        "finish_time": 2000,        # 调整结束时间
                        "max_silence_time": 2500,   # 调整静音时间
                        "min_speech_length": 200,   # 调整最小语音长度
                        "end_silence_length": 1000, # 调整结束静音长度
                        "continuous_speech": True,  # 启用连续语音
                        "max_merge_distance": 800   # 减小最大合并距离
                    },
                    "audio_config": {
                        "encoding": "pcm",
                        "voice_type": "NORMAL_FEMALE",
                        "speed_ratio": 0.92,        # 调整语速
                        "volume_ratio": 0.90,       # 调整音量
                        "pitch_ratio": 1.00,
                        "enable_subtitle": False,
                        "denoise": True,           # 启用降噪
                        "remove_silent": False     # 禁用静音移除
                    }
                }
            }

            print("发送音频数据到服务器")
            await ws_client.send(json.dumps(message))
            print("音频数据发送完成")
            return
        except Exception as e:
            print(f"第 {retry + 1} 次发送失败：{str(e)}")
            if retry < max_retries - 1:
                print("等待重试...")
                await asyncio.sleep(1)
            else:
                print("达到最大重试次数，发送失败")


def main():
    with gr.Blocks() as demo:
        gr.Markdown("语音助手")

        with gr.Row():
            api_key_input = gr.Textbox(label="API Key", type="password", placeholder="请输入您的API Key")
            connect_btn = gr.Button("建立连接")
            connection_status = gr.Textbox(label="连接状态", interactive=False)

        mic = gr.Audio(sources="microphone", type="filepath", label="麦克风输入")
        output_audio = gr.Audio(label="回复音频", streaming=True, autoplay=True)

        ws_client_state = gr.State(None)
        message_queue = asyncio.Queue()

        async def on_connect(api_key):
            if not api_key:
                return "API Key 不能为空"

            ws_client = await connect_and_receive(api_key, message_queue)
            if not ws_client:
                return "WebSocket 连接失败"

            ws_client_state.value = ws_client
            print("WebSocket 连接成功")
            return "WebSocket 连接成功"

        connect_btn.click(
            on_connect,
            inputs=api_key_input,
            outputs=connection_status,
        )

        async def on_audio(audio_file):
            if not audio_file:
                print("未接收到音频文件")
                return

            ws_client = ws_client_state.value
            if not ws_client or not ws_client.connection:
                print("未连接到服务器，请先建立连接。")
                return

            await send_audio_data(ws_client, audio_file)

        mic.stream(
            on_audio,
            inputs=[mic],
            outputs=None,
            stream_every=3,
            time_limit=360,
        )

        async def stream_audios():
            async for audio_chunk in audio_stream(message_queue):
                yield audio_chunk

        demo.load(
            stream_audios,
            inputs=None,
            outputs=output_audio,
        )

    demo.launch(share=True)


if __name__ == "__main__":
    main()