import pytest


def funP():
    return [[1, 2], [2, 3]]


class TestPara:

    @pytest.mark.parametrize("para1,para2", funP())
    def test_Param(self, para1, para2):
        print(f"获取的第一个参数为{para1},第二个参数为{para2}")
