import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config.settings import JWT_SECRET_KEY, JWT_EXPIRE_HOURS

class UserService:
    def __init__(self):
        self.secret_key = JWT_SECRET_KEY
        self.expire_hours = JWT_EXPIRE_HOURS

    def register_user(self, username, email, password):
        """注册新用户"""
        try:
            # 检查用户名和邮箱是否已存在
            if self._check_user_exists(username, email):
                raise ValueError("用户名或邮箱已存在")

            # 创建用户记录
            user = {
                "username": username,
                "email": email,
                "password": generate_password_hash(password),
                "created_at": datetime.datetime.utcnow(),
                "role": "user",
                "status": "active"
            }

            # TODO: 保存到数据库
            
            return {
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"]
            }

        except Exception as e:
            print(f"注册用户失败: {str(e)}")
            raise

    def login_user(self, email, password):
        """用户登录"""
        try:
            # TODO: 从数据库获取用户
            user = self._get_user_by_email(email)
            
            if not user:
                raise ValueError("用户不存在")

            if not check_password_hash(user["password"], password):
                raise ValueError("密码错误")

            # 生成JWT令牌
            token = self.generate_token(user)

            return {
                "token": token,
                "user": {
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }

        except Exception as e:
            print(f"用户登录失败: {str(e)}")
            raise

    def generate_token(self, user):
        """生成JWT令牌"""
        try:
            payload = {
                "user_id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=self.expire_hours)
            }
            
            return jwt.encode(payload, self.secret_key, algorithm="HS256")
            
        except Exception as e:
            print(f"生成令牌失败: {str(e)}")
            raise

    def verify_token(self, token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("令牌已过期")
        except jwt.InvalidTokenError:
            raise ValueError("无效的令牌")

    def get_user_profile(self, user_id):
        """获取用户资料"""
        try:
            # TODO: 从数据库获取用户资料
            user = self._get_user_by_id(user_id)
            
            if not user:
                raise ValueError("用户不存在")

            return {
                "username": user["username"],
                "email": user["email"],
                "avatar": user.get("avatar"),
                "role": user["role"],
                "created_at": user["created_at"],
                "usage_stats": self._get_user_usage_stats(user_id)
            }

        except Exception as e:
            print(f"获取用户资料失败: {str(e)}")
            raise

    def update_user_profile(self, user_id, data):
        """更新用户资料"""
        try:
            allowed_fields = ["username", "avatar", "password"]
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            if "password" in update_data:
                update_data["password"] = generate_password_hash(update_data["password"])

            # TODO: 更新数据库中的用户资料
            
            return {"message": "用户资料更新成功"}

        except Exception as e:
            print(f"更新用户资料失败: {str(e)}")
            raise

    def get_user_usage(self, user_id):
        """获取用户使用情况"""
        try:
            return {
                "audio_minutes": {
                    "used": 120,
                    "total": 300,
                    "remaining": 180
                },
                "history": self._get_user_history(user_id),
                "stats": self._get_user_usage_stats(user_id)
            }
        except Exception as e:
            print(f"获取用户使用情况失败: {str(e)}")
            raise

    def _check_user_exists(self, username, email):
        """检查用户名或邮箱是否已存在"""
        # TODO: 实现数据库查询
        return False

    def _get_user_by_email(self, email):
        """通过邮箱获取用户"""
        # TODO: 实现数据库查询
        return None

    def _get_user_by_id(self, user_id):
        """通过ID获取用户"""
        # TODO: 实现数据库查询
        return None

    def _get_user_history(self, user_id):
        """获取用户历史记录"""
        # TODO: 实现数据库查询
        return []

    def _get_user_usage_stats(self, user_id):
        """获取用户使用统计"""
        # TODO: 实现数据库查询
        return {
            "total_audio_generated": 0,
            "total_minutes": 0,
            "average_length": 0
        } 