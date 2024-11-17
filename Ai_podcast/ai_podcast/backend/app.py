from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import datetime
import io
from config.settings import CORS_ORIGINS, UPLOAD_FOLDER, SECRET_KEY
from services.dialogue_service import DialogueService
from services.outline_service import OutlineService
from services.audio_service import AudioService
from services.auth_service import AuthService
from utils.validation import allowed_file, validate_json_structure
from utils.file_utils import FileUtils
import os
import jwt

app = Flask(__name__, 
    static_folder='../frontend',
    static_url_path=''
)

app.config['SECRET_KEY'] = SECRET_KEY

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept", "Authorization"]
    }
})

# 认证服务实例
auth_service = AuthService()

# 认证相关路由
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({'error': '没有收到数据'}), 400
            
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not email or not password:
            return jsonify({'error': '邮箱和密码不能为空'}), 400
            
        # 验证用户
        user = auth_service.verify_user(email, password)
        if not user:
            return jsonify({'error': '邮箱或密码错误'}), 401
            
        # 生成 JWT token
        token = jwt.encode(
            {
                'user_id': user['id'],
                'email': user['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30 if remember else 1)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'email': user['email'],
                'username': user['username']
            }
        })
        
    except Exception as e:
        print(f"登录失败: {str(e)}")
        return jsonify({'error': '登录失败，请稍后重试'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data:
            return jsonify({'error': '没有收到数据'}), 400
            
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not all([email, password, username]):
            return jsonify({'error': '所有字段都是必填的'}), 400
            
        # 检查邮箱是否已存在
        if auth_service.check_email_exists(email):
            return jsonify({'error': '该邮箱已被注册'}), 409
            
        # 创建新用户
        user = auth_service.create_user(email, password, username)
        if not user:
            return jsonify({'error': '注册失败'}), 500
            
        return jsonify({
            'success': True,
            'message': '注册成功'
        })
        
    except Exception as e:
        print(f"注册失败: {str(e)}")
        return jsonify({'error': '注册失败，请稍后重试'}), 500

# 验证 token 的装饰器
def token_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': '没有提供认证令牌'}), 401
            
        try:
            token = token.split(' ')[1]  # Bearer token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = auth_service.get_user_by_id(data['user_id'])
            
            if not current_user:
                raise Exception('用户不存在')
                
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': '认证令牌已过期'}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'error': '无效的认证令牌'}), 401
            
    return decorated

# 原有的路由和功能保持不变
@app.route('/api/process', methods=['POST'])
@token_required
def process_content(current_user):
    try:
        print("\n【处理请求开始】")
        data = request.json
        if not data:
            return jsonify({'error': '没有收到数据'}), 400
            
        content = data.get('content')
        host = data.get('host', '张斌')
        expert = data.get('expert', '')
        dialogue_length = data.get('dialogueLength', 'long')

        print(f"\n【请求参数】")
        print(f"内容长度: {len(content) if content else 0} 字符")
        print(f"主持人: {host}")
        print(f"专家: {expert}")
        print(f"对话长度: {dialogue_length}")

        if not content:
            return jsonify({'error': '缺少内容'}), 400

        # 使用服务层处理业务逻辑
        print("\n【初始化服务】")
        outline_service = OutlineService()
        dialogue_service = DialogueService()
        
        # 如果没有提供专家名字，自动生成一个
        if not expert:
            print("\n【生成专家名字】")
            expert = outline_service.generate_expert_name(content)
            print(f"生成的专家名字: {expert}")
        
        print("\n【生成大纲】")
        outline = outline_service.generate_outline(content, host, expert, dialogue_length)
        if not outline:
            print("\n【错误】生成大纲失败")
            return jsonify({'error': '生成大纲失败'}), 500
            
        print("\n【生成对话】")
        print("开始处理完整对话...")
        result = dialogue_service.process_complete_dialogue(outline, content, host, expert)
        print(f"对话生成完成，包含 {len(result.get('script', []))} 段对话")
        
        print("\n【处理完成】")
        return jsonify(result)

    except Exception as e:
        print(f"\n【错误】处理失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {str(e)}")
        return jsonify({
            'error': str(e),
            'script': [{"role": "interviewer", "content": "很抱歉，生成过程中出现了错误。"}],
            'key_points': []
        }), 500

@app.route('/api/generate-audio', methods=['POST'])
@token_required
def generate_audio(current_user):
    try:
        data = request.json
        script = data.get('script')
        if not script:
            return jsonify({'error': '没有提供脚本内容'}), 400

        audio_service = AudioService()
        audio_data = audio_service.generate_complete_audio(script)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'podcast_{timestamp}.wav'
        
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/wav',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"音频生成失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-avatar', methods=['POST'])
@token_required
def upload_avatar(current_user):
    try:
        if 'avatar' not in request.files:
            return jsonify({'error': '没有文件'}), 400
            
        file = request.files['avatar']
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
            
        avatar_url = FileUtils.save_avatar(file)
        return jsonify({
            'success': True,
            'avatar_url': avatar_url
        })
        
    except Exception as e:
        print(f"上传头像失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
@app.route('/<path:path>')
def serve(path=''):
    try:
        if not path:
            return send_from_directory('../frontend', 'index.html')
        
        # 检查文件是否存在
        file_path = os.path.join('../frontend', path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            directory = os.path.dirname(path)
            filename = os.path.basename(path)
            return send_from_directory(f'../frontend/{directory}', filename)
        
        # 如果文件不存在，返回 index.html
        return send_from_directory('../frontend', 'index.html')
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return "File not found", 404

# 修改组件路由名称
@app.route('/components/<path:filename>')
def serve_component(filename):
    return send_from_directory('../frontend/components', filename)

# 修改静态文件路由名称，避免重复
@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('../frontend/static', filename)

# 添加页面路由
@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory('../frontend/pages', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 