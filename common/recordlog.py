import logging
import os
import time
from logging.handlers import RotatingFileHandler

# 按文件大小滚动备份

from conf import setting

log_path = setting.FILE_PATH["LOG"]
if not os.path.exists(log_path):
    os.mkdir(log_path)

logfile_name = log_path + r"\test.{}.log".format(time.strftime("%Y%m%d"))  # format可以只填充{}的字段


# print(logfile_name)


class RecordLog:

    def output_loggin(self):
        logger = logging.getLogger(__name__)  # __name__ 当前模块的名称
        # 防止重复
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s'
            )
            # 输出到指定文件
            fh = RotatingFileHandler(filename=logfile_name, mode='a', maxBytes=5242880,
                                     backupCount=7,
                                     encoding='utf-8')  # maxBytes:控制单个日志文件的大小，单位是字节,backupCount:用于控制日志文件的数量
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            logger.addHandler(fh)

            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)

        return logger


apilog = RecordLog()
logs = apilog.output_loggin()
