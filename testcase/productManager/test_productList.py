import allure
import pytest

from base.apiutil import BaseRequests
from common.readYaml import readTestCase
from common.recordlog import logs


@allure.feature("商品接口")  # allure报告功能名
class TestProduct:

    # @allure.story("商品请求信息")  # 用例名
    @pytest.mark.parametrize("base_info,testcase",
                             readTestCase("./testcase/productManager/productList.yaml"))  # 传入yaml文件中的参数
    def test_product(self, base_info, testcase):
        # logs.info(f"参数化为:{params}")
        # print("传递参数为", params)
        allure.dynamic.title(testcase["case_name"])
        BaseRequests().specification_yaml(base_info, testcase)

    # @allure.story("商品详情信息")
    @pytest.mark.parametrize("base_info,testcase", readTestCase("./testcase/productManager/productDetail.yaml"))
    def test_get_product_detail(self, base_info, testcase):
        allure.dynamic.title(testcase["case_name"])
        BaseRequests().specification_yaml(base_info, testcase)
