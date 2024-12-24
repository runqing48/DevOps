from mysql_tools.common_delete import build_delete_sql
from mysql_tools.common_insert import build_insert_sql
from mysql_tools.common_select import build_query_sql
from mysql_tools.common_update import build_update_sql
from mysql_tools.common_utils.common_pool_sql import execute_database_operation
from tencent_cloud.tencent_sdk.tencent_sdk import tencent_sdk


# 从数据库中获取当前的地域信息，返回一个字典形式的数据
def get_current_regions_from_db(user_id, cloud_provider_id):
    master_table = "cloud_regions"  # 查询的主表名
    # 确定要查询的列，格式：(表名.列名, 别名)
    columns = ["cloud_regions.region_code", "cloud_regions.region_name", "cloud_regions.region_state"]
    where = f"cloud_regions.user_id = {user_id} AND cloud_regions.cloud_provider_id = {cloud_provider_id}"
    query_sql = build_query_sql(master_table=master_table, columns=columns, where=where)
    result = execute_database_operation(query_sql, operation_type="query")
    return {row["region_code"]: row for row in result}

# 拉取腾讯云的地域信息，比对当前库信息后判断是否需要存入库中
def save_tencent_regions(user_id, cloud_provider_id):
    # API请求地址
    endpoint = "cvm.tencentcloudapi.com"
    # 拿到返回值
    region_data = tencent_sdk(endpoint)

    # region_data 是字符串，需要解析
    if isinstance(region_data, str):
        import json
        region_data = json.loads(region_data)

    # 获取腾讯云的地域信息
    current_regions = {region["Region"]: region for region in region_data["RegionSet"]}

    # 获取当前数据库中的地域信息
    db_regions = get_current_regions_from_db(user_id, cloud_provider_id)

    # 需要插入或更新的地域数据
    insert_data = []
    update_data = []
    delete_data = []

    for region_code, region in current_regions.items():
        # 如果地域已经存在，且数据有变动，更新它
        if region_code in db_regions:
            db_region = db_regions[region_code]
            if region["RegionName"] != db_region["region_name"] or region["RegionState"] != db_region["region_state"]:
                update_data.append(region)
        else:
            # 如果地域不存在，则插入新记录
            insert_data.append({
                "user_id": user_id,
                "cloud_provider_id": cloud_provider_id,
                "region_code": region["Region"],
                "region_name": region["RegionName"],
                "region_state": region["RegionState"]
            })

    # 删除数据库中已不存在的地域
    for region_code, db_region in db_regions.items():
        if region_code not in current_regions:
            delete_data.append(db_region)

    # 执行插入操作
    if insert_data:
        insert_sql = build_insert_sql("cloud_regions", insert_data)
        insert_result = execute_database_operation(insert_sql, insert_data, operation_type="insert")
        print(f"插入了 {insert_result} 条记录")

    # 执行更新操作
    for region in update_data:
        table = "cloud_regions"

        # 更新操作
        update_data = {"region_name": f"{region["RegionName"]}", "region_state":f"{region["RegionState"]}"}
        where_condition = f"region_code = '{region["Region"]}'"  # 直接拼接WHERE条件

        update_sql, params = build_update_sql(table, update_data, where_condition)
        update_result = execute_database_operation(update_sql, params, operation_type="update")
        print(f"更新了 {update_result} 条记录")

    # 执行删除操作
    for region_code, db_region in db_regions.items():
        # 如果数据库中的地域在腾讯云的地域中找不到，执行删除
        if region_code not in current_regions:
            delete_conditions = f"region_code = '{db_region['region_code']}'"  # 使用 db_region['region_code'] 来获取地域代码
            delete_sql = build_delete_sql("cloud_regions", delete_conditions)
            delete_result = execute_database_operation(delete_sql, operation_type="delete")
            print(f"删除了 {delete_result} 条记录")



if __name__ == "__main__":
    user_id = 1
    cloud_provider_id = 1
    save_tencent_regions(user_id, cloud_provider_id)
