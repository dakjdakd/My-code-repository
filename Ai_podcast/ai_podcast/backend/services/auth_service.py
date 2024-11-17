import hashlib
import uuid
from typing import Optional, Dict

class AuthService:
    def __init__(self):
        # 临时使用内存存储用户数据，实际应该使用数据库
        self.users = {}
        
    def hash_password(self, password: str) -> str:
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def verify_user(self, email: str, password: str) -> Optional[Dict]:
        """验证用户登录"""
        user = self.users.get(email)
        if user and user['password'] == self.hash_password(password):
            return user
        return None
        
    def check_email_exists(self, email: str) -> bool:
        """检查邮箱是否已被注册"""
        return email in self.users
        
    def create_user(self, email: str, password: str, username: str) -> Dict:
        """创建新用户"""
        if self.check_email_exists(email):
            raise ValueError('邮箱已被注册')
            
        user = {
            'id': str(uuid.uuid4()),
            'email': email,
            'username': username,
            'password': self.hash_password(password)
        }
        
        self.users[email] = user
        return user
        
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """通过用户ID获取用户信息"""
        for user in self.users.values():
            if user['id'] == user_id:
                return user
        return None 