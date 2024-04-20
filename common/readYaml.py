import yaml
import requests
import os
import jsonpath
from conf.setting import FILE_PATH
from common.recordlog import logs


def readTestCase(file):
    resultList = []
    try:
        with open(file, "r", encoding="UTF-8") as f:
            yaml_data = yaml.safe_load(f)[0]
            baseInfo = yaml_data.get("baseInfo")
            testcases = yaml_data.get("testCase")
            for tc in yaml_data.get("testCase"):
                # print("每个测试用例为",tc)
                param = [baseInfo, tc]
                resultList.append(param)

            return resultList
    except Exception as e:
        print("文件打开失败", e)


class ReadYamlData:  # 与yaml文件进行交互
    def __init__(self, yame_file=None):  # 如果没有传参就为默认值
        if yame_file is not None:
            self.yaml_file = yame_file
        else:
            self.yaml_file = "../testcase/Login/login.yaml"

    def write_yaml_data(self, value, file_path="extract.yaml"):
        # file_path = "extract.yaml"  # 接口依赖传递数据
        if not os.path.exists(file_path):  # 在当前工作目录寻找
            os.system(file_path)

        try:
            file = open(file_path, "a", encoding="utf-8")
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
                # logs.info("写入extract文件成功")
            else:
                print("写入的类型必须为dict字典类型")
        except Exception as e:
            print(e)
        finally:  # 手动关闭文件
            file.close()

    def get_extract_yaml(self, node_name):
        file_path = FILE_PATH["extract"]  # 获取配置中的
        if os.path.exists(file_path):
            pass
        else:
            print("extract.yaml不存在")
            file = open(file_path, "w")
            file.close()
            print("创建成功")

        with open(file_path, "r", encoding="utf-8") as rf:
            extract_data = yaml.safe_load(rf)
            print(f"提取出的{node_name}为:{extract_data}")
            print("读取出的底层原生extract_data为", extract_data[node_name])
        return extract_data[node_name]

    def clear_yaml_data(self):
        with open(FILE_PATH["extract"], "w") as f:
            f.truncate()  # 清除数据


if __name__ == '__main__':
    res = readTestCase("../testcase/Login/login.yaml")[0]
    print(res)
    # print(res["testCase"][0]["validation"][0]["contains"])
    host_url = "http://localhost:8787"

    url = host_url + res["baseInfo"]["url"]
    method = res["baseInfo"]["method"]
    header = res["baseInfo"]["header"]
    data = res["testCase"][0]["data"]

    print(data)
    res = requests.request(method=method, url=url, data=data, headers=header)
    tokenStr = jsonpath.jsonpath(res.json(), "$.token")
    print(res.json())
    print("响应的token为:", tokenStr[0])

    OperateYaml = ReadYamlData()
    # writeToken = {"token": tokenStr[0]}  # 注意:tokenStr是个列表
    # OperationYaml.write_yaml_data(writeToken,"extract.yaml")
    a = OperateYaml.get_extract_yaml("product_id")
    print(a)
