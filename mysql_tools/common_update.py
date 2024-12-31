# 示例调用
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建 UPDATE SQL 语句
def build_update_sql(table, update_data, where=None):
    """
    构建 UPDATE SQL 语句，支持通过字符串拼接 WHERE 子句。

    :param table: 表名
    :param data: 更新的数据，格式：{"col1": value1, "col2": value2}
    :param where: 查询的 WHERE 条件，格式："column = value AND column2 = value2"
    :return: 完整的 UPDATE SQL 语句
    """
    set_clause = ", ".join([f"{col} = %({col})s" for col in update_data.keys()])  # SET 部分
    params = {}  # 用于存储参数

    # 将更新的数据添加到参数字典中
    params.update(update_data)  # 合并 update_data 到 params

    # 如果提供了 WHERE 条件，直接拼接 WHERE 部分
    sql = f"UPDATE {table} SET {set_clause}"
    if where:
        sql += f" WHERE {where}"

    return sql, params


# 调用
if __name__ == "__main__":
    table = "user_cloud_keys"  # 查询的主表名

    # 更新操作
    update_data = {"secret_key": "1592283349"}
    where_condition = "id = 8 AND cloud_provider = 'aws'"  # 直接拼接WHERE条件

    update_sql, params = build_update_sql(table, update_data, where_condition)
    print("构建的 UPDATE SQL:", update_sql)

    update_result = execute_database_operation(update_sql, params, operation_type="update")
    print("修改操作影响行数：", update_result)

