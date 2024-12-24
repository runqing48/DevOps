# 示例调用
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建查询 SQL 语句
def build_query_sql(master_table, columns=None, joins=None, where=None, group_by=None, order_by=None, limit=None,
                    offset=None):
    """
    动态构建查询 SQL 语句，支持复杂的条件，连接，排序，分组，分页等。
    :param master_table: 主表名称
    :param columns: 要查询的列，格式：["table_name.column_name", "alias"]
    :param joins: 连接的表和条件，格式：[("JOIN", "table_name", "ON ...")]
    :param where: 查询的条件字符串，支持复杂条件，格式："column = value AND column2 = value2"
    :param group_by: 分组字段，格式：["column1", "column2"]
    :param order_by: 排序字段，格式：["column ASC|DESC"]
    :param limit: 查询的条数
    :param offset: 查询的偏移
    :return: 完整的 SQL 查询语句和参数字典
    """

    params = {}  # 用于存储参数
    # 1. 构建 SELECT 子句
    if not columns:
        columns = [f"{master_table}.*"]
    select_clause = ", ".join(columns)

    # 2. 构建 FROM 子句（主表）
    sql = f"SELECT {select_clause} FROM {master_table}"


    # 3. 构建 JOIN 子句
    if joins:
        for join_type, join_table, on_condition in joins:
            sql += f" {join_type} {join_table} ON {on_condition}"

    # 4. 构建 WHERE 子句
    if where:
        sql += f" WHERE {where}"


    # 5. 构建 GROUP BY 子句
    if group_by:
        sql += f" GROUP BY {', '.join(group_by)}"

    # 6. 构建 ORDER BY 子句
    if order_by:
        sql += f" ORDER BY {', '.join(order_by)}"

    # 7. 构建 LIMIT 子句
    if limit:
        sql += f" LIMIT {limit}"

    # 8. 构建 OFFSET 子句
    if offset:
        sql += f" OFFSET {offset}"

    return sql


# 调用
if __name__ == "__main__":
    master_table = "user_cloud_keys"  # 查询的主表名
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = ["user_cloud_keys.id", "user_cloud_keys.cloud_provider", "users.user_id", "users.username"]
    joins = [("INNER JOIN", "users", "user_cloud_keys.user_id = users.user_id")]  # 这里要附带上表名
    where = "user_cloud_keys.user_id = 1 AND user_cloud_keys.cloud_provider = 'AWS'"

    query_sql = build_query_sql(master_table=master_table, columns=columns, where=where, joins=joins)
    print("构建的查询 SQL:", query_sql)

    result = execute_database_operation(query_sql, operation_type="query")
    print("查询结果:", result)
