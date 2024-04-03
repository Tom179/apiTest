import allure
import pytest

from base.apiutil import BaseRequests
from common.readYaml import readTestCase
from common.recordlog import logs


@allure.feature("物流项目接口")  # allure报告功能名
class TestLogistic:

    @pytest.mark.parametrize("base_info,testcase",
                             readTestCase("./testcase/logistic/getMaterial.yaml"))  # 传入yaml文件中的参数
    def test_get_material(self, base_info, testcase):
        # logs.info(f"参数化为:{params}")
        # print("传递参数为", params)
        allure.dynamic.title(testcase["case_name"])
        BaseRequests().specification_yaml(base_info, testcase)
