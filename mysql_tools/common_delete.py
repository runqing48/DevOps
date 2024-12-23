from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建 DELETE SQL 语句
def build_delete_sql(table, conditions):
    """
    构建 DELETE SQL 语句。

    :param table: 表名
    :param conditions: WHERE 条件，格式：{"col": value}
    :return: 完整的 DELETE SQL 语句
    """
    where_clause = " AND ".join([f"{col} = %({col})s" for col in conditions.keys()])  # WHERE 部分
    sql = f"DELETE FROM {table} WHERE {where_clause}"

    return sql


if __name__ == "__main__":
    table = "user_cloud_keys"

    # 删除操作
    delete_conditions = {"id": 6}
    delete_sql = build_delete_sql(table, delete_conditions)
    print("构建的 DELETE SQL:", delete_sql)
    delete_result = execute_database_operation(delete_sql, delete_conditions, operation_type="delete")
    print("删除操作影响行数:", delete_result)
