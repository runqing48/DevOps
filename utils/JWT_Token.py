import jwt
import datetime
from django.conf import settings


# 用于生成JWT Token的函数
def generate_jwt_token(users):
    # 设置JWT的有效期（例如1小时）
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # JWT的payload部分
    payload = {
        'user_id': users.user_id,
        'email': users.email,
        'exp': expiration_time  # 设置过期时间
    }

    # 使用密钥和算法生成JWT Token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token