# 示例调用
from mysql_tools.common_utils.common_pool_sql import execute_database_operation


# 动态构建查询 SQL 语句，支持复杂的 WHERE 条件，AND/OR 连接
def build_query_sql(master_table, columns=None, conditions=None, joins=None, order_by=None, group_by=None, limit=None, offset=None,
                    subquery=None):
    """
    构建动态的 SQL 查询语句，支持复杂的 WHERE 条件，支持 AND/OR 连接。

    :param master_table: 查询的主表名
    :param columns: 需要查询的列，格式：[("table_name.column_name", "alias")]
    :param conditions: 查询的条件字典，支持 AND/OR 连接，格式：{"field1": value1, "field2": value2, "condition": "AND"}
    :param joins: 连接的表和条件，格式：[("JOIN", "table_name", "ON ...")]
    :param order_by: 排序字段（例如：["user_id", "ASC"]）
    :param group_by: 分组字段（例如：["column1", "column2"]）
    :param limit: 查询结果的限制（例如：10，表示只返回前 10 条数据）
    :param offset: 分页偏移（例如：10，表示从第 10 条开始）
    :param subquery: 子查询，如果是子查询，直接插入 SQL 语句
    :return: 完整的 SQL 查询语句
    """
    # 如果 columns 为空，选择默认的所有列
    if not columns:
        columns = [f"{table}.*"]

    # 构建 SELECT 子句
    select_columns = [f"{col}" if len(col) > 1 else col for col in columns]
    sql = f"SELECT {', '.join(select_columns)} FROM {table}"

    # 构建 JOIN 子句
    if joins:
        for join_type, join_table, on_condition in joins:
            sql += f" {join_type} {join_table} ON {on_condition}"

    params = {}  # 用于存储参数
    # 构建 WHERE 子句
    if conditions:
        where_clauses = []

        for idx, (field, value) in enumerate(conditions.items()):
            # 每个条件后面可能有连接符 AND/OR
            condition = value.get('value', value)  # 如果条件是字典，取出实际值
            connector = value.get('connector', 'AND') if isinstance(value, dict) else 'AND'  # 默认连接符为 AND

            # 判断条件类型
            if isinstance(condition, tuple):
                if len(condition) == 2 and condition[0] == "in":
                    # IN 条件
                    where_clauses.append(
                        f"{field} IN ({', '.join([f'%({field}_{i})s' for i in range(len(condition[1]))])})")
                    for i, val in enumerate(condition[1]):
                        params[f"{field}_{i}"] = val  # 把 IN 的值放到参数里，使用不同的占位符
                elif len(condition) == 2 and condition[0] == "between":
                    # BETWEEN 条件
                    where_clauses.append(f"{field} BETWEEN %({field})s AND %({field}_end)s")
                    params[field] = condition[1][0]  # BETWEEN 起始值
                    params[f"{field}_end"] = condition[1][1]  # BETWEEN 结束值
                elif len(condition) == 2 and condition[0] == "like":
                    # LIKE 条件
                    where_clauses.append(f"{field} LIKE %({field})s")
                    params[field] = f"%{condition[1]}%"  # 处理 LIKE 匹配
                elif len(condition) == 2 and condition[0] == "not in":
                    # NOT IN 条件
                    where_clauses.append(f"{field} NOT IN ({', '.join(['%(' + field + ')s' for _ in condition[1]])})")
                    params[field] = condition[1]  # 把 NOT IN 的值放到参数里
                elif len(condition) == 2 and condition[0] == "not between":
                    # NOT BETWEEN 条件
                    where_clauses.append(f"{field} NOT BETWEEN %({field})s AND %({field}_end)s")
                    params[field] = condition[1][0]  # NOT BETWEEN 起始值
                    params[f"{field}_end"] = condition[1][1]  # NOT BETWEEN 结束值
                else:
                    # 普通等于（=）条件
                    where_clauses.append(f"{field} = %({field})s")
                    params[field] = condition[1]  # 设置实际值
            elif condition is None:
                # IS NULL 条件
                where_clauses.append(f"{field} IS NULL")
            elif isinstance(condition, str) and condition.upper() == "NOT NULL":
                # IS NOT NULL 条件
                where_clauses.append(f"{field} IS NOT NULL")
            else:
                # 普通的等于（=）条件
                where_clauses.append(f"{field} = %({field})s")
                params[field] = condition  # 设置实际值

            # 如果不是第一个条件，添加连接符 AND/OR
            if idx > 0:
                where_clauses[-1] = f"{connector} " + where_clauses[-1]

        sql += " WHERE " + " ".join(where_clauses)

    # 添加子查询（如果有）
    if subquery:
        sql += f" {subquery}"

    # 构建 GROUP BY 子句
    if group_by:
        sql += f" GROUP BY {', '.join(group_by)}"

    # 构建 ORDER BY 子句
    if order_by:
        sql += f" ORDER BY {order_by[0]} {order_by[1]}"

    # 构建 LIMIT 子句
    if limit:
        sql += f" LIMIT {limit}"

    # 构建 OFFSET 子句
    if offset:
        sql += f" OFFSET {offset}"

    return sql, params  # 返回 SQL 和参数字典


# 调用
if __name__ == "__main__":
    table = "user_cloud_keys"  # 查询的主表名
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = [
        "user_cloud_keys.id",
        "user_cloud_keys.cloud_provider",
        "users.user_id",
        "users.username"
    ]
    # 复杂查询，包含多表联查、排序、分页等
    # IN, NOT IN, BETWEEN, NOT BETWEEN, LIKE, IS NULL, IS NOT NULL。
    # 通过字典中的条件类型来确定使用哪种 SQL 运算符。
    conditions = {
        "user_cloud_keys.id": {"value": 1, "connector": "AND"},
        "user_cloud_keys.cloud_provider": {"value": "Tencent", "connector": "OR"},
        "user_cloud_keys.user_id": {"value": ("in", [1, 2, 3]), "connector": "AND"}
    }  # where查询条件，要确定表明
    joins = [("INNER JOIN", "users", "user_cloud_keys.user_id = users.user_id")]  # 这里要附带上表名
    order_by = ["users.user_id", "ASC"]  # 这里要附带上表名
    limit = 10
    offset = 0
    group_by = ["user_cloud_keys.cloud_provider"]

    query_sql, params = build_query_sql(table, columns, conditions, joins, order_by, group_by, limit, offset)
    print("构建的查询 SQL:", query_sql)
    print("参数:", params)

    result = execute_database_operation(query_sql, params, operation_type="query")
    print("查询结果:", result)
