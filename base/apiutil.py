from json.decoder import JSONDecodeError
import urllib3
from requests import utils
import allure
import requests
import re
import jsonpath
from common.readYaml import ReadYamlData, readTestCase
import json
from common.debugTalk import DebufTalk
from common.recordlog import logs
from conf.oprateConfig import OprateConfig
from common.assertion import Assertion
import common.debugTalk

assert_res = Assertion()


# 最好写一个request类，把日志封装到一起
class BaseRequests:
    def __init__(self):
        self.OprateYaml = ReadYamlData()
        self.OprateConf = OprateConfig()

    def replace_laod(self, data):  # 解析表达式
        print("进入replace_load")
        '''yaml文件解析${}'''
        str_data = data  # ？
        if not isinstance(data, str):  # 判断是否为字符串类型，是的话就转换为json字符串
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):  # 循环2次
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("$")  # 找到表达式的开始位置
                end_index = str_data.index('}', start_index)

                exp = str_data[start_index:end_index + 1]  # 提取表达式
                print("提取表达式", exp)

                func_name = exp[2:exp.index("(")]  # 提取函数名
                print("获取函数名", func_name)

                func_params = exp[exp.index('(') + 1:exp.index(')')]  # 提取出参数值
                print("获取参数名", func_params)

                print("spilt结果为", func_params.split(','))
                if len(func_params.split(',')) > 1:
                    print("提取键大于1")
                    extract_data = getattr(DebufTalk(), func_name)(*func_params.split(',') if func_params else "")
                else:
                    print("提取键小于1")
                    extract_data = getattr(DebufTalk(), func_name)(*func_params.split(',') if func_params else "")
                    # print("extract_data")
                    # extract_data = DebufTalk().get_extract_data("Cookie")
                # getattr返回一个类的方法或属性，如果是方法的话会执行该方法

                print("调用解析函数", extract_data)  # 传入替换参数对应的值

                str_data = str_data.replace(exp, str(extract_data))
                print("replace后的str_data为", str_data)

        if data and isinstance(data, dict):
            data = json.loads(str_data)
            print("替换后的data为", data, "替换后的类型为", type(data))
        else:
            print("替换后的data不是字典")
            data = str_data
        return data

    def specification_yaml(self, base_info, test_case):  # 规范yaml测试接口
        print("调用一次specification_yaml")
        # print("每个测试用例为:",test_case)
        '''
        :param yaml_dict:列表类型
        :return:
        '''
        params_type = ["params", "data", "json"]

        # try:#加上try_catch可能无法捕获Assertion错误
        base_url = self.OprateConf.get_envi("host")
        url = base_url + base_info["url"]
        api_name = base_info["api-name"]
        method = base_info["method"]
        header = base_info["header"]
        print(api_name)

        # attach展示必须要字符串
        allure.attach(url, f"接口地址:{url}", allure.attachment_type.TEXT)  # 第二个参数是消息展示的格式， 字符串+s 表示格式化,个性化配置allure输出
        allure.attach(api_name, f"接口名称:{api_name}", allure.attachment_type.TEXT)
        allure.attach(str(header), f"请求头:{str(header)}", allure.attachment_type.TEXT)
        allure.attach(method, f"请求方法:{method}", allure.attachment_type.TEXT)

        print("构造参数")

        case_name = test_case.pop("case_name")
        val = self.replace_laod(test_case.get("validation"))
        test_case["validation"] = json.loads(val)  # 替换之后要把字符串重新转换为dict对象
        validation = test_case.pop("validation")
        # print("validation为", validation)
        extract = test_case.pop("extract", None)
        extract_list = test_case.pop("extract_list", None)
        for key, value in test_case.items():  # 遍历dict中的所有键值对
            if key in params_type:  # 如果属于param、data、json格式
                test_case[key] = self.replace_laod(value)  # 解析,重写获取字典
        print("-----------------------------")
        print("testcase为", test_case)
        print("获取到的test_case长度为", len(test_case.keys()))
        Params = {}
        if len(test_case.keys()) != 0:
            print("有参数，构造请求头，参数类型")
            ArgType = list(test_case.keys())[0]  # 获取参数类型，params、data、json
            Params = {
                ArgType: test_case[ArgType],
                # "cookies": cookie["access_token_cookie"]  # 有问题
            }  # 获取不定类型的参数
            print("参数：", test_case[ArgType])
            logs.info(f"参数类型{ArgType}")

        cookie = {}
        print(type(cookie))
        if "cookies" in base_info:  # 如果键存在
            # print("cookie键存在")
            # print("用例信息中有设置cookie，开启语法分析替换")
            cookieStr = self.replace_laod(base_info["cookies"])  # 解析表达式获取cookie
            stripped_string = cookieStr.strip("'")
            cookieStr = stripped_string.replace("'", "\"")
            # print("cookieStr为：", cookieStr)

            cookie = json.loads(cookieStr)
            # print("转换为字典后的cookie为", cookie)
            # print("cookie type", type(cookie))
            # print("提取出的用例base_info为", base_info)
            # Params["cookies"] = cookie["access_token_cookie"]  # 有问题

        allure.attach(str(Params), f"请求参数:{str(Params)}", allure.attachment_type.TEXT)
        print("发起请求↑")
        # request请求的可选参数**kwargs传入一个**字典就可以
        res = requests.request(url=url, **Params, headers=header, method=method, cookies=cookie, files=None)
        print("接收响应")
        set_cookie = requests.utils.dict_from_cookiejar(res.cookies)  # 写入cookie
        if set_cookie:
            print("cookie类型为：", type(cookie))
            print("set_cookie为", set_cookie)
            cookie["Cookie"] = set_cookie
            self.OprateYaml.write_yaml_data(cookie)
            logs.info(f"cookie{cookie}")

        # 每个用例发送请求
        resTxt = res.text
        resJson = res.json()
        print("响应为:", resJson)
        # print("响应信息的内容为:", type(resTxt))
        allure.attach(resTxt, f"接口响应信息:", allure.attachment_type.TEXT)
        allure.attach(str(res.status_code), f"接口状态码: {res.status_code}", allure.attachment_type.TEXT)

        if extract is not None:
            self.extract_data(extract, resTxt)

        if extract_list is not None:
            self.extract_data_list(extract_list, resTxt)
        # 处理断言
        print("调用一次assert_result")
        assert_res.assert_result(validation, resJson, res.status_code)

    # except Exception as e:  # 抛出异常会显示在测试报告中
    #     logs.error(f"抛出异常{e}")
    #     print(e)
    #     return e

    def extract_data(self, testcase_extract, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extract:  yaml中的extract值
        :param response:  实际响应值
        :return:
        """

        pattern_list = ["(.+?)", "(.*?)", r"(\d+)", r"(\d*)"]
        try:
            for key, value in testcase_extract.items():
                # print("遍历extract值:", key, value)
                # #正则表达式
                # for pat in pattern_list:
                #     if pat in value:  # 该表达式中包含正则表达式
                #         # print(pat)
                #         # 表达式，从哪儿提取
                #         ext_list = re.search(value, response)
                #         print(ext_list)
                #         if pat in [r"(\d+)", r"(\d*)"]:
                #             extract_data = {key: int(ext_list.group(1))}  # 返回的ext_list是一个Match匹配对象，要用group来获取匹配字符串
                #         else:
                #             extract_data = {key: ext_list.group(1)}
                #         logs.info(f"正则表达式提取到的参数:{extract_data}")
                #         self.OprateYaml.write_yaml_data(extract_data, "../extract.yaml")
                # 处理json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]  # 获取提取出的信息
                    # print("jsonpath提取出的信息为:", ext_json)
                    if ext_json:
                        extract_data = {key: ext_json}
                    else:
                        extract_data = {key: "未提取到"}

                    logs.info(f"json提取:{extract_data}")
                    self.OprateYaml.write_yaml_data(extract_data, "./extract.yaml")
        except:
            logs.error("接口返回值异常")

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.OprateYaml.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)  # 根据表达式提取值
                    logs.info(f'提取的参数为:{ext_json}')
                    # print("jsonpath提取出的信息为", ext_json)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.OprateYaml.write_yaml_data(extract_date, "./extract.yaml")
        except Exception as e:
            logs.error(f'{e}:接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    b = BaseRequests()
    data = readTestCase("../testcase/Login/login.yaml")[0]  # 读取不到
    b.specification_yaml(data)
