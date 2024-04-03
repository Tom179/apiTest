import pytest
from common.readYaml import readTestCase
from base.apiutil import BaseRequests
import allure

from common.recordlog import logs


@allure.feature("登录接口")  # allure报告功能名
class TestLogin:

    # @allure.story("用户名密码登录正确")  # 用例名
    @pytest.mark.order(1)
    @pytest.mark.parametrize("base_info,testcase", readTestCase("./testcase/Login/login.yaml"))  # 传入yaml文件中的参数
    def test_Login01(self, base_info, testcase):
        # logs.info(f"参数化为:{params}")
        # print("传递参数为", params)
        allure.dynamic.title(testcase["case_name"])
        BaseRequests().specification_yaml(base_info, testcase)
    #
    # @allure.story("用户名密码登录错误")  # 用例名
    # @pytest.mark.parametrize("base_info,testcase", readTestCase("./testcase/Login/login.yaml"))
    # def test_Login02(self, base_info, testcase):
    #     # print("传递参数为", )
    #     BaseRequests().specification_yaml(base_info, testcase)
