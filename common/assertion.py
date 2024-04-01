from common.recordlog import logs
import jsonpath
import allure
import os
from common.readYaml import readTestCase
from common.connect import ConnectMysql


class Assertion:
    """接口断言封装
    1.字符串包含
    2.结果相等断言
    3.结果不相等断言
    4.断言接回返回值里面的任意一个值
    5.数据库断言
    【断言标识，0代表成功】
    """

    def contains_assert(self, value, response, status_code):  # 字符串包含，响应码等于判断
        flag = 0
        for assert_key, assert_value in value.items():  # value.item为{"status_code":200}}
            # print("判断类型:", assert_key, "是否为", assert_value)
            if assert_key == "status_code":  # 判断的类型,响应码
                if assert_value != status_code:
                    flag += 1
                    logs.error(f"contains断言失败,实际响应状态码{status_code}不等于预期值{assert_value}")
                else:
                    logs.info(f"{assert_key}包含断言成功")
                allure.attach(f"判断字段{assert_key} 预期结果{assert_value} 实际结果{status_code}", "包含断言status_code",
                              allure.attachment_type.TEXT)
            else:  # 其他类型，jsonPath
                print(f"从真实resp中判断{assert_key}")
                resp_list = jsonpath.jsonpath(response, f"$..{assert_key}")  # 实际响应的值
                # resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)  # 实际响应的值
                # print("resp_list", resp_list)
                # print("resp_list", resp_list[0])
                # 全部转为字符串
                if isinstance(resp_list[0], str):
                    resp_list = "".join(resp_list)
                if resp_list[0] is None:
                    resp_list = "None"
                if resp_list:
                    print(resp_list)
                    if assert_value in resp_list:  # 如果实际   响应中包含了预期
                        # print("断言成功")
                        logs.info(f"{assert_key}包含断言成功")
                    else:
                        flag += 1
                        logs.error(f"contains断言失败,实际结果{resp_list}不包含预期值{assert_value}")
                allure.attach(f"判断字段{assert_key} 预期结果{assert_value} 实际结果{resp_list}", "包含断言值",
                              allure.attachment_type.TEXT)
        return flag  # 返回断言错误数？

    def equal_assert(self, value, response):  # 两个dict，一个预期值，一个响应值。如何判断
        flag = 0
        if isinstance(value, dict) and isinstance(response, dict):
            for eqKey in value.keys():  # value是yaml中的预期键值
                if response[eqKey] != value[eqKey]:  # 要预期键存在，且值相等才行
                    flag += 1
                    logs.error("相等断言失败")
                    return flag
            logs.info("相等断言成功")
            # resList = []
            # eqKey = list(value.keys())[0]
            # for resKey in response:
            #     if resKey != eqKey:
            #         resList.append(resKey)
            #
            # for rl in resList:  # 构造出和value结构相同的response
            #     del response[rl]  # del可以删除各种元素，键值对
            # print("response构造：", response)
            # if operator.eq(value, response):
            #     print("相等断言通过")
            # else:
            #     flag += 1
            # print("resList:", resList)
        else:
            logs.error("相等断言失败")
            raise TypeError("value和response必须为字典类型")
        return flag

    # def not_equal_assert(self):
    #     pass

    def assert_result(self, expected, response, status_code):
        """
        :param expected:预期结果
        :param response:实际响应结果
        :param status_code:实际状态码
        :return:
        """
        all_flag = 0  # 断言成功标识
        for oneExpected in expected:  # 拿到yaml表中每一个断言模式：contains、eq等
            for assType, value in oneExpected.items():  # 拿到断言模式中具体的键值
                if assType == "contains":
                    flag = self.contains_assert(value, response, status_code)
                    all_flag += flag
                elif assType == "eq":
                    flag = self.equal_assert(value, response)
                    all_flag += flag
                elif assType == "db":
                    self.assert_mysql(value)
                    all_flag += flag

        assert all_flag == 0

    def assert_mysql(self, expected_sql):
        """
        :param expected_sql:yaml中的sal语句
        :return:
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_sql)
        if db_value is not None:
            logs.info("数据库断言成功")
        else:
            flag += 1
            logs.error("数据库断言失败")

        return flag


if __name__ == '__main__':
    # yamlCase = readTestCase("E:/pycharmWorks/day04/testcase/Login/login.yaml")
    yamlPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"testcase\Login", "login.yaml")
    print(yamlPath)
    yamlCase = readTestCase(yamlPath)[0]
    print(type(yamlCase))
    validateCase = yamlCase["testCase"][0]["validation"][2]["eq"]
    print(validateCase)
    response = {
        "error_code": None,
        "msg": "登录成功",
        "msg_code": 200,
        "token": "2adfpafdausadof"
    }

    assert Assertion().equal_assert(validateCase, response) == 0
    print("断言测试成功")
