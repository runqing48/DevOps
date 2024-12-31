from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)  # 对应 user_id，AutoIncrement
    username = models.CharField(max_length=255, unique=True)  # 对应 username，唯一索引
    created_at = models.DateTimeField(auto_now_add=True)  # 对应 created_at，自动设置为当前时间
    email = models.EmailField(max_length=255)  # 对应 email
    password = models.CharField(max_length=255)  # 对应 password

    class Meta:
        db_table = 'users'  # 映射到原有的 users 表

    def __str__(self):
        return self.username
