import requests
import json

# API 地址
url = "http://localhost:7860/v1/tts"

# 请求体数据
data = {
  "text": "你好，这是一个文本到语音的测试。你觉得如何呢？",
  "chunk_length": 200,
  "format": "wav",
  "voice": "111",
  "mp3_bitrate": 64,
  "references": [],
  "reference_id": None,
  "seed": None,
  "use_memory_cache": "never",
  "normalize": True,
  "opus_bitrate": -1000,
  "latency": "normal",
  "streaming": False,
  "max_new_tokens": 1024,
  "top_p": 0.7,
  "repetition_penalty": 1.2,
  "temperature": 0.7,
  "seed":121312,
  "style":"angry"
}

# 发送POST请求
response = requests.post(url, json=data)

# 检查响应状态码
if response.status_code == 200:
    # 如果返回的是音频数据，保存为文件
    with open('output2.wav', 'wb') as f:
        f.write(response.content)
    print("音频文件已保存为 output2.wav")
else:
    # 输出错误信息
    print(f"请求失败: {response.status_code}")
    print(response.text)
