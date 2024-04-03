# python 3.8
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


def generateSign():
    timestamp = str(round(time.time() * 1000))
    secret = "SEC28e43a55001641c8804b1ced0d4cb389ec7ad686fe974d038b488376ea3791b3"  # 钉钉机器人需要的密钥
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign


def send_dingding_msg(content, at_all=True):
    """
    推送消息
    :param content: 发送内容
    :param at_all: 是否@所有人
    :return:
    """
    timestamp_sign = generateSign()
    # 需要钉钉的webhook地址,构造url+timestamp+sign "url&timestamp=***&sign=***"
    url = f'https://oapi.dingtalk.com/robot/send?access_token=5fb58d20fa27ab2f7c752e925b51dc06c6590110cb9fc685e7f30ec9272917e2&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'
    # print(url)
    headers = {"Content-type": "application/json;charset=utf-8"}
    req_data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "isAtAll": at_all
        }
    }
    res = requests.post(url=url, json=req_data, headers=headers)
    print(res.text)
    print(res.json())
    return res.text


if __name__ == '__main__':

    for i in range(3):
        content = f"""
        各位好，第次{i}次测试的执行结果如下：
        XXX
        点击查看测试报告:www.baidu.com
        """
        # print(content)
        # send_dingding_msg("你好")
        send_dingding_msg(content)
