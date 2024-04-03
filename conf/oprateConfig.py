import configparser
from conf.setting import FILE_PATH


class OprateConfig:  # 读取ini配置文件

    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = FILE_PATH["conf"]
            print("self.__filepath为", self.__file_path)
        else:
            self.__file_path = file_path

        self.conf = configparser.ConfigParser()  # 这个工具读取ini格式的配置文件
        try:
            self.conf.read(self.__file_path, encoding="utf-8")
        except Exception as e:
            print(e)

    def get_section_for_data(self, section, option):
        """
         :param section: ini头部值
        :param option: 选项值的key
        :return:
        """
        try:
            data = self.conf.get(section, option)
            return data
        except Exception as e:
            print("出现错误", e)

    def get_envi(self, option):
        return self.get_section_for_data("api_envi", option)

    def get_mysql(self, option):
        return self.get_section_for_data("MYSQL", option)

    def get_jenkins(self, option):
        return self.get_section_for_data("JENKINS", option)


if __name__ == '__main__':
    op = OprateConfig()
    print(op.get_mysql("port"))
    # print("属性字典", vars(op))
    # print(op.get_section_for_data('MYSQL', 'host'))
    # print(op.get_envi("host"))
