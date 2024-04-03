import json
import re
import jenkins
from conf.oprateConfig import OprateConfig

conf = OprateConfig()


class OperJenkins:
    def __init__(self):
        self.__config = {
            "url": conf.get_jenkins("url"),
            "username": conf.get_jenkins("username"),
            "password": conf.get_jenkins("password"),
            "timeout": conf.get_jenkins("timeout")
        }

        self.__server = jenkins.Jenkins(**self.__config)
        self.job_name = conf.get_jenkins("job_name")

    def get_job_number(self):
        build_number = self.__server.get_job_info(self.job_name).get("lastBuild").get("number")
        return build_number

    def get_build_job_status(self):
        buildNum = self.get_job_number()
        job_status = self.__server.get_job_info(self.job_name, buildNum).get("result")  # 获取构建完的最新的构建状态
        return job_status

    def get_console_log(self):
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_job_description(self):
        description = self.__server.get_job_info(self.job_name).get("description")
        url = self.__server.get_job_info(self.job_name).get("url")
        return description, url

    def get_build_report(self):
        report = self.__server.get_build_test_report(self.job_name, self.get_job_number())
        return report

    def report_success_or_fail(self):
        report_info = self.get_build_report()
        console_log = self.get_console_log()
        report_line = re.search(r"http://192.168.****/jog/jjapi/(.*?)allure", console_log).group(0)

        return report_line

