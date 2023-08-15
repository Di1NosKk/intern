import requests
import json
import os

payload = {'content': '', 'type':''}

# self test with long length of content 
# contents = []
# with open("/home/albay/djs/data/测试数据.txt") as f_in:
#         data = f_in.readlines()
#         for line in data:
#             try:
#                 contents.append(line.split('\n')[0])
#             except(IndexError) as e:
#                 pass
# for content in contents:
#     content.strip()
# a = "".join(contents)
# payload = {'content': a, 'type':1}


# self test with input 
print("请输入文本：")
payload['content'] = input()

print("\n目的：\n1. 摘要\n2. 分词\n3. 敏感信息过滤\n4. 文本信息分类\n5. 关键词抽取\n6. 实体识别\n7. 文本聚类")
print("请输入目的：")
payload['type'] = int(input())

r = requests.post('http://192.168.10.52:10002', data=json.dumps(payload))

print(r.text)
