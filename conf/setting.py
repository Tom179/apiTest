# 管理整个框架的脚本目录
import os
import sys
import logging

DIR_PATH = os.path.dirname(os.path.dirname(__file__))  # 取整个项目的根目录 __file__是特殊的python变量，表示当前路径
sys.path.append(DIR_PATH)  # 将当前路径添加到python解释器的搜索路径中


# 日志配置
LOG_LEVEL = logging.DEBUG  # 输出到文件
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台级别

FILE_PATH = {
    'extract': os.path.join(DIR_PATH, "extract.yaml"),
    "conf": os.path.join(DIR_PATH, "conf", "conf.ini"),  # ??写死的拼接方式，配置的ini文件默认位置
    "LOG": os.path.join(DIR_PATH, "log")
}

# print(DIR_PATH)
# print("FILE_PATH为:", FILE_PATH)
# print("config.ini文件的路径为", FILE_PATH["conf"])
# print("extract文件的路径为", FILE_PATH["extract"])
