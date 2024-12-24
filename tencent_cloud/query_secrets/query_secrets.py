from mysql_tools.common_select import build_query_sql
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


def query_secret(user_id, cloud_id):
    master_table = "cloud_keys"  # 查询的主表名
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = ["cloud_keys.cloud_id", "cloud_keys.user_id", "cloud_keys.secret_key", "cloud_keys.secret_id"]
    where = f"cloud_keys.cloud_id = {cloud_id} AND cloud_keys.user_id = {user_id}"

    query_sql = build_query_sql(master_table=master_table, columns=columns, where=where)

    result = execute_database_operation(query_sql, operation_type="query")
    if result and len(result) == 1:
        secret_key = result[0]["secret_key"]
        secret_id = result[0]["secret_id"]
        return secret_key, secret_id
    else:
        print("查询内容出错！")
        return None

if __name__ == "__main__":
    secret_key, secret_id = query_secret(1, 1)
    print(secret_key, secret_id)
