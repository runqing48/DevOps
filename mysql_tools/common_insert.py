from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建 INSERT SQL 语句
def build_insert_sql(table, data):
    """
    构建 INSERT SQL 语句，支持批量插入。

    :param table: 表名
    :param data: 插入的数据，格式：[{"col1": value1, "col2": value2}, {...}]
    :return: 完整的 INSERT SQL 语句
    """
    if not data:
        return ""

    columns = ", ".join(data[0].keys())  # 获取字段名
    values_placeholder = ", ".join([f"%({col})s" for col in data[0].keys()])  # 获取占位符
    sql = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholder})"

    return sql


if __name__ == "__main__":
    table = "user_cloud_keys"  # 插入的表名
    # 插入操作
    insert_data = [
        {"user_id": 1, "cloud_provider": "AWS", "secret_id": "120", "secret_key": "120"}
        # {"user_id": 1, "cloud_provider": "AWS", "secret_id": "110", "secret_key": "110"}
    ]
    insert_sql = build_insert_sql(table, insert_data)
    print("构建的 INSERT SQL:", insert_sql)
    insert_result = execute_database_operation(insert_sql, insert_data, operation_type="insert")
    print("插入操作影响行数：", insert_result)
