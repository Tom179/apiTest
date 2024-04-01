import pytest
import os
import shutil

if __name__ == '__main__':
    pytest.main()
    shutil.copy("environment.xml", "./report/temp")  # 复制文件
    os.system("allure serve ./report/temp")
