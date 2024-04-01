import allure
import pytest

from base.apiutil import BaseRequests
from common.readYaml import readTestCase
from common.recordlog import logs


@allure.feature("商品接口")  # allure报告功能名
class TestProduct:

    @allure.story("商品请求信息")  # 用例名
    @pytest.mark.parametrize("params", readTestCase("./testcase/productManager/productList.yaml"))  # 传入yaml文件中的参数
    def test_product(self, params):
        # logs.info(f"参数化为:{params}")
        # print("传递参数为", params)
        BaseRequests().specification_yaml(params)

    @allure.story("商品详情信息")
    @pytest.mark.parametrize("params", readTestCase("./testcase/productManager/productDetail.yaml"))
    def test_get_product_detail(self, params):
        BaseRequests().specification_yaml(params)
