import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# CORS 配置
CORS_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5001",
    "http://127.0.0.1:5001",
    "*"
]

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# JWT 密钥配置
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')  # 从环境变量获取，如果没有则使用默认值

# API配置
ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
API_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
# 添加 TTS API 的基础 URL（临时）
TTS_BASE_URL = "http://localhost:8000"  # 这里先用一个临时的地址

if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY 未设置！请检查 .env 文件。")

# 文件上传配置
UPLOAD_FOLDER = 'static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CORS配置
CORS_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5001",
    "http://127.0.0.1:5001",
    "*"
] 