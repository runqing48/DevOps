# 判断用户是否已存在
from mysql_tools.common_insert import build_insert_sql
from mysql_tools.common_select import build_query_sql
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


class User:
    def __init__(self, user_id, username, created_at, email, password):
        self.user_id = user_id
        self.username = username
        self.created_at = created_at
        self.email = email
        self.password = password  # 这里存储加密后的密码


# 创建用户
def create_user(username, email, passwd):
    table = "users"  # 插入的表名
    # 插入操作
    insert_data = [
        {"username": f"{username}", "email": f"{email}", "password": f"{passwd}"}
        # {"user_id": 1, "cloud_provider": "AWS", "secret_id": "110", "secret_key": "110"}
    ]
    insert_sql = build_insert_sql(table, insert_data)
    insert_result = execute_database_operation(insert_sql, insert_data, operation_type="insert")
    if insert_result == 1:
        return True
    else:
        return False

# 验证邮箱是否已存在
def is_email(email):
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = ["count(user_id)"]
    where = f"users.email = '{email}'"

    query_sql = build_query_sql(master_table="users", columns=columns, where=where)

    result = execute_database_operation(query_sql, operation_type="query")
    if result[0]['count(user_id)'] >= 1:
        return True
    else:
        return False


# 根据用户邮箱和密码查询的结果判断是否登录
def is_users(email):
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = ["users.user_id", "users.username", "users.created_at", "users.email", "users.password"]
    where = f"users.email = '{email}'"

    query_sql = build_query_sql(master_table="users", columns=columns, where=where)

    result = execute_database_operation(query_sql, operation_type="query")
    if len(result) == 1:
        return result
    else:
        return None