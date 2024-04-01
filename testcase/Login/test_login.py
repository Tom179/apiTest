import pytest
from common.readYaml import readTestCase
from base.apiutil import BaseRequests
import allure

from common.recordlog import logs


@allure.feature("登录接口")  # allure报告功能名
class TestLogin:

    @allure.story("用户名密码登录正确")  # 用例名
    @pytest.mark.parametrize("params", readTestCase("./testcase/Login/login.yaml"))  # 传入yaml文件中的参数
    def test_Login01(self, params):
        # logs.info(f"参数化为:{params}")
        print("传递参数为", params)
        BaseRequests().specification_yaml(params)

    # @allure.story("用户名密码登录错误")  # 用例名
    # @pytest.mark.parametrize("params", readTestCase("./testcase/Login/login.yaml"))
    # def test_Login02(self, params):
    #     print("传递参数为", params)
    #     BaseRequests().specification_yaml(params)
