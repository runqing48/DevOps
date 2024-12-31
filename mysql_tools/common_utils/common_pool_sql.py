import asyncio
import aiomysql
import configparser
import os

# 配置MySQL连接池
# 获取 common_pool_sql.py 文件的绝对路径
common_pool_sql_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前脚本的目录路径
# 拼接出 config.ini 的绝对路径
config_path = os.path.join(common_pool_sql_path, '../../conf', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
dbconfig = {
    "host": config['database']['host'],
    "user": config['database']['user'],
    "password": config['database']['password'],
    "database": config['database']['database']
}

# 创建数据库连接池
async def create_async_pool():
    return await aiomysql.create_pool(
        host=dbconfig["host"],
        port=3306,
        user=dbconfig["user"],
        password=dbconfig["password"],
        db=dbconfig["database"],
        minsize=1,
        maxsize=10
    )

# 通用执行 SQL 操作的方法
async def execute_sql(sql, data=None, fetch=False):
    pool = await create_async_pool()  # 使用 await 来获取连接池
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            try:
                # 开始事务
                await conn.begin()

                # 执行SQL操作
                if data:
                    await cursor.executemany(sql, data) if isinstance(data, list) else await cursor.execute(sql, data)
                else:
                    await cursor.execute(sql)

                # 提交事务
                await conn.commit()

                # 如果是查询操作，返回结果
                if fetch:
                    result = await cursor.fetchall()
                    return result

                # 返回影响的行数（对于插入、更新、删除操作）
                return cursor.rowcount

            except Exception as e:
                # 回滚事务
                await conn.rollback()
                print(f"SQL 执行失败: {e}")
                return None

# 封装的查询操作
async def query_data(sql, params=None):
    return await execute_sql(sql, params, fetch=True)

# 封装的插入操作
async def insert_data(sql, data):
    return await execute_sql(sql, data, fetch=False)

# 封装的更新操作
async def update_data(sql, data):
    return await execute_sql(sql, data, fetch=False)

# 封装的删除操作
async def delete_data(sql, params):
    return await execute_sql(sql, params, fetch=False)

# 外部接口封装，方便外部直接调用
def execute_database_operation(sql, params=None, operation_type="insert"):
    """
    外部调用接口，用于执行不同类型的 SQL 操作（插入、查询、更新、删除）。
    :param sql: SQL 语句
    :param params: SQL 参数
    :param operation_type: 操作类型 (insert, query, update, delete)
    :return: 查询结果（如果操作是查询）
    """
    # 根据操作类型调用相应的函数
    if operation_type == "insert":
        return asyncio.run(insert_data(sql, params))
    elif operation_type == "query":
        return asyncio.run(query_data(sql, params))
    elif operation_type == "update":
        return asyncio.run(update_data(sql, params))
    elif operation_type == "delete":
        return asyncio.run(delete_data(sql, params))
    else:
        print("不支持的操作类型")
        return None
