import json
import requests
#payload = {"prompt":"你是谁","history":[]}
#payload = {"content":"我是一个来自中国的学生","type":4}
payload = {"content":"算力成本涨了多少，从英伟达GPU芯片的交付价格即可一窥。目前，AI算力中最关键的芯片GPU被英伟达垄断，市场占有率达到90%以上。以英伟达GPU芯片A100为例，该芯片价格从去年12月开始上涨，截至今年4月上半月，其5个月价格累计涨幅达到37.5%；同期A800价格累计涨幅达20%。同时，英伟达GPU交货周期也被拉长，之前拿货周期大约为一个月，现在基本都需要三个月或更长。甚至，部分新订单"可能要到12月才能交付"。","type":6}
#json.loads(payload)
r = requests.post("http://101.36.73.75:10002",data=json.dumps(payload))
print(r.text)
