import os
from werkzeug.utils import secure_filename
import datetime
from config.settings import UPLOAD_FOLDER

class FileUtils:
    @staticmethod
    def save_avatar(file):
        """保存上传的头像文件"""
        try:
            if file.filename == '':
                raise ValueError("文件名为空")
                
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"avatar_{timestamp}.{filename.rsplit('.', 1)[1].lower()}"
            
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(file_path)
            
            return f"/static/uploads/avatars/{new_filename}"
            
        except Exception as e:
            print(f"保存头像失败: {str(e)}")
            raise 