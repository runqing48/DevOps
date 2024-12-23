# 示例调用
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建 UPDATE SQL 语句
def build_update_sql(table, data, conditions):
    """
    构建 UPDATE SQL 语句。

    :param table: 表名
    :param data: 更新的数据，格式：{"col1": value1, "col2": value2}
    :param conditions: WHERE 条件，格式：{"col": value}
    :return: 完整的 UPDATE SQL 语句
    """
    set_clause = ", ".join([f"{col} = %({col})s" for col in data.keys()])  # SET 部分
    where_clause = " AND ".join([f"{col} = %({col})s" for col in conditions.keys()])  # WHERE 部分
    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

    return sql


# 调用
if __name__ == "__main__":
    table = "user_cloud_keys"  # 查询的主表名

    # 更新操作
    update_data = {"cloud_provider": "Google"}
    update_conditions = {"id": 6}
    update_sql = build_update_sql(table, update_data, update_conditions)
    print("构建的 UPDATE SQL:", update_sql)
    update_result = execute_database_operation(update_sql, {**update_data, **update_conditions}, operation_type="update")
    print("修改操作影响行数：", update_result)

