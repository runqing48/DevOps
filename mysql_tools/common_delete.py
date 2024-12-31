from mysql_tools.common_utils.common_pool_sql import execute_database_operation

# 动态构建 DELETE SQL 语句
def build_delete_sql(table, where=None):
    """
    构建 DELETE SQL 语句，支持通过字符串拼接 WHERE 子句。

    :param table: 表名
    :param where: 查询的 WHERE 条件，格式："column = value AND column2 = value2"
    :return: 完整的 DELETE SQL 语句
    """
    sql = f"DELETE FROM {table}"

    # 如果提供了 WHERE 条件，直接拼接 WHERE 部分
    if where:
        sql += f" WHERE {where}"

    return sql


if __name__ == "__main__":
    table = "user_cloud_keys"

    # 删除条件
    delete_conditions = "id = 8 AND cloud_provider = 'AWS'"  # 直接拼接WHERE条件

    delete_sql = build_delete_sql(table, delete_conditions)
    print("构建的 DELETE SQL:", delete_sql)

    delete_result = execute_database_operation(delete_sql, operation_type="delete")
    print("删除操作影响行数:", delete_result)
