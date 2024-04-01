from json.decoder import JSONDecodeError

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

assert_res = Assertion()


# 最好写一个request类，把日志封装到一起
class BaseRequests:
    def __init__(self):
        self.OprateYaml = ReadYamlData()
        self.OprateConf = OprateConfig()

    def replace_laod(self, data):  # 解析表达式
        '''yaml文件解析${}'''
        str_data = data  # ？
        if not isinstance(data, str):  # 判断是否为字符串类型，是的话就转换为json字符串
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):  # 循环2次
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("$")  # 找到表达式的开始位置
                end_index = str_data.index('}', start_index)

                exp = str_data[start_index:end_index + 1]  # 提取表达式
                # print(exp)

                func_name = exp[2:exp.index("(")]  # 提取函数名

                func_params = exp[exp.index('(') + 1:exp.index(')')]  # 提取出参数值
                # print(func_params)

                extract_data = getattr(DebufTalk(), func_name)(*func_params.split(',') if func_params else "")
                # getattr返回一个类的方法或属性，如果是方法的话会执行该方法

                # print(extract_data)  # 传入替换参数对应的值

                str_data = str_data.replace(exp, str(extract_data))
                # print(str_data)

        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, yaml_dict):  # 规范yaml测试接口
        '''
        :param yaml_dict:列表类型
        :return:
        '''
        params_type = ["params", "data", "json"]

        # try:#加上try_catch可能无法捕获Assertion错误
        base_url = self.OprateConf.get_envi("host")
        url = base_url + yaml_dict["baseInfo"]["url"]
        api_name = yaml_dict["baseInfo"]["api-name"]
        method = yaml_dict["baseInfo"]["method"]
        header = yaml_dict["baseInfo"]["header"]
        print(api_name)

        # attach展示必须要字符串
        allure.attach(url, f"接口地址:{url}", allure.attachment_type.TEXT)  # 第二个参数是消息展示的格式， 字符串+s 表示格式化,个性化配置allure输出
        allure.attach(api_name, f"接口名称:{api_name}", allure.attachment_type.TEXT)
        allure.attach(str(header), f"请求头:{str(header)}", allure.attachment_type.TEXT)
        allure.attach(method, f"请求方法:{method}", allure.attachment_type.TEXT)

        cookie = None
        try:
            cookie = self.replace_laod(yaml_dict["baseInfo"]["cookies"])  # 解析表达式获取cookie
        except:
            pass

        # print("用例列表？的类型为:", type(case_info["testCase"]), "\n值为\n", case_info["testCase"])

        for tc in yaml_dict["testCase"]:  # 字典中有‘-’的为列表的元素值，tc为列表中的元素：测试用例
            case_name = tc.pop("case_name")  # 列表删除指定元素的值
            validation = tc.pop("validation")
            extract = tc.pop("extract", None)
            extract_list = tc.pop("extract_list", None)  # 没有默认返回None,所以允许该键不存在
            # print("每个testcase的值取出后为:", tc)

            for key, value in tc.items():  # 遍历dict中的所有键值对
                if key in params_type:  # 如果属于param、data、json格式
                    tc[key] = self.replace_laod(value)  # 解析,重写获取字典
                    # print(tc[key])
                    # print(value)

            # print(tc.keys())
            # print(list(tc.keys()))

            ArgType = list(tc.keys())[0]  # 获取参数类型，params、data、json
            Params = {
                ArgType: tc[ArgType]
            }  # 获取不定类型的参数

            allure.attach(str(Params), f"请求参数:{str(Params)}", allure.attachment_type.TEXT)
            # request请求的可选参数**kwargs传入一个**字典就可以
            res = requests.request(url=url, **Params, headers=header, method=method, cookies=cookie,
                                   files=None)

            # 每个用例发送请求
            resTxt = res.text
            resJson = res.json()
            # print("响应信息的内容为:", type(resTxt))
            allure.attach(resTxt, f"接口响应信息:", allure.attachment_type.TEXT)
            allure.attach(str(res.status_code), f"接口状态码: {res.status_code}", allure.attachment_type.TEXT)

            # print(res.json())
            # print(extract)

            if extract is not None:
                self.extract_data(extract, resTxt)

            if extract_list is not None:
                self.extract_data_list(extract_list, resTxt)

            # 处理断言
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
