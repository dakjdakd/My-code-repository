import requests
import msgpack
import io
import wave
import time
import base64
import json
from config.settings import TTS_BASE_URL

class AudioService:
    def __init__(self):
        self.base_url = TTS_BASE_URL
        self.interviewer_reference = None
        self.expert_reference = None

    def generate_complete_audio(self, script):
        """生成完整的播客音频"""
        try:
            print("开始生成完整音频...")
            all_audio_data = []
            
            # 生成参考音频
            self._generate_reference_audio()
            
            # 生成每段对话的音频
            for segment in script:
                audio_data = self._generate_segment_audio(segment)
                all_audio_data.append(audio_data)
                
            # 合并音频片段
            print("合并所有音频片段...")
            combined_audio = self._combine_wav_segments(all_audio_data)
            print(f"音频生成完成，总大小: {len(combined_audio)} bytes")
            return combined_audio
            
        except Exception as e:
            print(f"生成完整音频时出错: {str(e)}")
            raise

    def _generate_reference_audio(self):
        """生成参考音频"""
        if not self.interviewer_reference:
            print("生成主持人参考音频...")
            self.interviewer_reference = self._generate_audio_with_retry(
                "您好，我是今天的主持人",
                is_interviewer=True
            )
            
        if not self.expert_reference:
            print("生成专家参考音频...")
            self.expert_reference = self._generate_audio_with_retry(
                "您好，我是今天的特邀专家",
                is_interviewer=False
            )

    def _generate_segment_audio(self, segment):
        """生成单个对话片段的音频"""
        text = segment['content']
        is_interviewer = segment['role'] == 'interviewer'
        print(f"生成{'主持人' if is_interviewer else '专家'}的音频...")
        
        return self._generate_audio_with_retry(text, is_interviewer)

    def _generate_audio_with_retry(self, text, is_interviewer, max_retries=3, retry_delay=2):
        """带重试机制的音频生成函数"""
        for attempt in range(max_retries):
            try:
                print(f"正在尝试生成音频... (尝试 {attempt + 1}/{max_retries})")
                
                payload = {
                    "text": text,
                    "format": "wav",
                    "reference_audio": [
                        base64.b64encode(self.interviewer_reference).decode() if is_interviewer 
                        else base64.b64encode(self.expert_reference).decode()
                    ] if self.interviewer_reference and self.expert_reference else None,
                    "reference_text": [
                        "您好，我是今天的主持人" if is_interviewer 
                        else "您好，我是今天的特邀专家"
                    ] if self.interviewer_reference and self.expert_reference else None,
                    "temperature": 0.1,
                    "seed": 12345 if is_interviewer else 67890,
                    "chunk_length": 200,
                    "normalize": True,
                    "latency": "normal"
                }
                
                response = requests.post(
                    f"{self.base_url}/v1/tts",
                    data=msgpack.packb(payload),
                    headers={'Content-Type': 'application/msgpack'}
                )
                
                if response.status_code == 200:
                    print("音频生成成功!")
                    return response.content
                    
                if response.status_code == 502:
                    print(f"服务器暂时不可用 (502)，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                    
                raise Exception(f"TTS API 返回错误: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"网络错误: {str(e)}，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                raise Exception(f"网络连接失败: {str(e)}")
                
        raise Exception(f"生成音频失败，已重试 {max_retries} 次")

    def _combine_wav_segments(self, audio_segments):
        """合并WAV格式的音频片段"""
        try:
            if not audio_segments:
                raise Exception("没有音频片段可合并")
                
            output = io.BytesIO()
            
            with wave.open(io.BytesIO(audio_segments[0]), 'rb') as first_wav:
                params = first_wav.getparams()
                
                with wave.open(output, 'wb') as out_wav:
                    out_wav.setparams(params)
                    
                    for segment in audio_segments:
                        with wave.open(io.BytesIO(segment), 'rb') as wav:
                            out_wav.writeframes(wav.readframes(wav.getnframes()))
            
            return output.getvalue()
            
        except Exception as e:
            print(f"合并WAV文件失败: {str(e)}")
            raise

    def save_audio_file(self, audio_data, filename):
        """保存音频文件到磁盘"""
        try:
            with open(filename, 'wb') as f:
                f.write(audio_data)
            print(f"音频文件已保存: {filename}")
        except Exception as e:
            print(f"保存音频文件失败: {str(e)}")
            raise

    def get_audio_duration(self, audio_data):
        """获取音频时长(秒)"""
        try:
            with wave.open(io.BytesIO(audio_data), 'rb') as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception as e:
            print(f"获取音频时长失败: {str(e)}")
            return 0

    def validate_audio_quality(self, audio_data):
        """验证音频质量"""
        try:
            with wave.open(io.BytesIO(audio_data), 'rb') as wav:
                # 检查采样率
                if wav.getframerate() != 44100:
                    print("警告: 采样率不是44.1kHz")
                
                # 检查声道数
                if wav.getnchannels() != 1:
                    print("警告: 不是单声道音频")
                
                # 检查采样位深
                if wav.getsampwidth() != 2:
                    print("警告: 采样位深不是16位")
                
                return True
        except Exception as e:
            print(f"音频质量验证失败: {str(e)}")
            return False