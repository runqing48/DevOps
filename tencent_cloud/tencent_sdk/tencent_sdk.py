
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
from tencent_cloud.query_secrets.query_secrets import query_secret

# 查询密钥
secret_key, secret_id = query_secret(1, 1)


def tencent_sdk(endpoint, region=None, params=None):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(secret_id, secret_key)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = endpoint

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        if region:
            client = cvm_client.CvmClient(cred, region, clientProfile)
        else:
            client = cvm_client.CvmClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeRegionsRequest()
        if params:
            params = params
        else:
            params = {}
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeRegionsResponse的实例，与请求对象对应
        resp = client.DescribeRegions(req)
        # 输出json格式的字符串回包
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        print(err)