from common.readYaml import ReadYamlData
import random


class DebufTalk:
    def __init__(self):
        self.OperateYaml = ReadYamlData()

    def get_extract_order_data(self, data, ramdoms):  # 根据索引获取data
        if ramdoms not in [0, -1, -2]:
            return data[ramdoms - 1]

    def get_extract_data(self, node_name, randoms=None):
        '''
        :param node_name: 文件中的key
        :param random: 随机读取extract.yaml中的数据
        '''
        data = self.OperateYaml.get_extract_yaml(node_name)  # 根据键名获取extract中间文件的结果
        # print(data)
        if randoms is not None:
            randomKey = int(randoms)
            data_value = {
                randomKey: self.get_extract_order_data(data, randomKey),
                0: random.choice(data),
                -1: ",".join(data),  # 全部结果字符串
                -2: data,  # 全部结果的列表
                # 正数，根据下标返回
            }
            data = data_value[randomKey]
            # print(f"提取出的{node_name}为:{data}")

        return data

    def md5_params(self, params):
        return "md5加密" + str(params)


if __name__ == '__main__':
    debug = DebufTalk()
    print(debug.get_extract_data("token", -2))
    print(debug.get_extract_data("goodsId", 0))
