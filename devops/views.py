import json

import bcrypt
from django.http import JsonResponse
from utils.JWT_Token import generate_jwt_token
from .models import User
from .users.users import is_email, create_user, is_users


def user_signup(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 数据
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # 检查邮箱是否已存在
            if is_email(email):
                return JsonResponse({'message': '用户已存在'}, status=400)

            # 创建用户
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if create_user(username, email, hashed_password.decode('utf-8')):
                return JsonResponse({'message': '用户注册成功！'}, status=201)
            else:
                return JsonResponse({'message': '用户注册失败！'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)


def user_login(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 数据
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # 获取用户数据
            user_data = is_users(email)
            user_data = user_data[0]
            if user_data:
                # 获取加密密码
                stored_pass = user_data['password']

                if bcrypt.checkpw(password.encode('utf-8'), stored_pass.encode('utf-8')):
                    user = User(
                        user_id=user_data['user_id'],
                        username=user_data['username'],
                        created_at=user_data['created_at'],
                        email=user_data['email'],
                        password=stored_pass
                    )
                    token = generate_jwt_token(user)
                    return JsonResponse({
                        'success': True,
                        'token': token
                        }, status=201)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': '密码错误'
                    }, status=401)
            else:
                return JsonResponse({
                    'success': False,
                    'message': '用户不存在'
                }, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)