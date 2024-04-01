import pytest
from common.readYaml import ReadYamlData


# 要在与pytest同级目录下才生效

@pytest.fixture(scope='session', autouse=True)  # 配置全局固件
def fixture_test():
    print("---------前----------")
    yield
    print("---------后----------")


OperateYaml = ReadYamlData()


@pytest.fixture(scope="session", autouse=True)  # 每次测试函数都用
def clear_extract_data():
    OperateYaml.clear_yaml_data()
