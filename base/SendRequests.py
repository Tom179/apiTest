# import requests
#
#
# # 定义一个函数，接收各种参数
# def sendRequest(url, **kwargs):
#     response = requests.request(url=url, **kwargs)
#     return response
#
#
# # 设置其他参数，例如 headers、method、cookie 等
# header = {'Content-Type': 'application/json;charset=UTF-8'}
# method = 'POST'
# argType = "json"
#
# # 构建请求参数字典
# request_params = {
#     "url": "http://8.130.97.3:81/addBook",
#     argType: {
#         "bookName": "Arg测试",
#         "author": "Arg测试",
#         "number": 1092
#     },  # 可以根据需要动态传递不同的数据
#     'headers': header,
#     # 'method': method,
# }
#
# # 发送请求
# response = sendRequest(method="POST", **request_params)
