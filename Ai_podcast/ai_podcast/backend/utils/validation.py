from config.settings import ALLOWED_EXTENSIONS

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_json_structure(data):
    """验证JSON基本结构"""
    if not isinstance(data, dict):
        raise ValueError("返回格式必须是JSON对象")
    
    if 'script' not in data or 'key_points' not in data:
        raise ValueError("JSON必须包含script和key_points字段")
    
    if not isinstance(data['script'], list) or not isinstance(data['key_points'], list):
        raise ValueError("script和key_points必须是数组")
    
    dialogue_count = len(data['script'])
    if dialogue_count < 60:
        raise ValueError(f"对话数严重不足：要求至少60句对话，当前只有{dialogue_count}句！") 