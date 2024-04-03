import pytest
from common.readYaml import ReadYamlData
from common.dingdingRobot import send_dingding_msg
from common.operJenkins import OperJenkins


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

#
# def pytest_terminal_summary(terminalreporter, exitstatus, config):  # pytest内置方法，固定名称固定写法
#     """
#     :param terminalreporter: 内部终端报告对象，对象的status属性
#     :param exitstatus:
#     :param config:
#     :return:
#     """
#
#     print("terminalreporter为:", terminalreporter.stats)
#     case_total = terminalreporter._numcollected  # 这些所谓的报告结果是从何而来？pytest断言自动收集的
#     print("总数", case_total)
#     passed = len(terminalreporter.stats.get("passed", []))
#     print("通过用例为", passed)
#     failed = len(terminalreporter.stats.get("failed", []))
#     print("失败用例为", failed)
#     erro = len(terminalreporter.stats.get("error", []))
#     print("错误为", erro)
#
#     #需要部署到Jenkins持续集成中运行
#     oper=OperJenkins()
#     report=oper.report_success_or_fail()
#
#     reportContent = f"""
#         本次测试报告结果如下:
#         测试用例总数{case_total},
#         通过数{passed},
#         失败数{failed},
#         错误数{erro},
#         点击查看测试报告{report},
#     """
#     send_dingding_msg(reportContent)

