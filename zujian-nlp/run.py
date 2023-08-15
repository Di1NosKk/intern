
from fastapi import FastAPI, Request
import json
import uvicorn, json, datetime
import torch
import sys
import os
import time
from paddlenlp import Taskflow

# script_path = os.path.abspath(__file__)
# this_dir = os.path.dirname(script_path)
# sys.path.append(this_dir)
# sys.path.insert(0, this_dir + '/Pytorch_Bert_TextCNN_CLS/')
# import predict
from summarization import get_textrank4zh_summarization_str, get_textrank4zh_keywords
from segmentation import word_segmentation
from sensitive import filter_sensitive
from text_ner import ner_exec
import clueClassify
import multi_tags

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

# classification = predict.classifier()
clueAI = clueClassify.ClueAI()

multiTag = multi_tags.Tag()
tags = [['财经', '财经是指财政与经济，如：他对财经方面的问题非常有研究。'],['股票', '股票（stock、shares）是股份公司所有权的一部分，也是发行的所有权凭证，是股份公司为筹集资金而发行给各个股东作为持股凭证并借以取得股息和红利的一种有价证券。股票是资本市场的长期信用工具'],['基金', '基金，英文是fund，广义是指为了某种目的而设立的具有一定数量的资金。主要包括公积金、信托投资基金、保险基金、退休基金，各种基金会的基金。'],['外汇', '外汇，英文名是Foreign currency，是货币行政当局（中央银行、货币管理机构、外汇平准基金及财政部）以银行存款、财政部库券、长短期政府证券等形式保有的在国际收支逆差时可以使用的债权。'],['科技', '社会上习惯于把科学和技术连在一起，统称为科学技术，简称科技。实际二者既有密切联系，又有重要区别。科学解决理论问题，技术解决实际问题。科学要解决的问题，是发现自然界中确凿的事实与现象之间的关系，并建立理论把事实与现象联系起来'],['手机', '手机，全称为移动电话或无线电话，通常称为手机，原本只是一种通讯工具，早期又有“大哥大”的俗称 [1] ，是可以在较广范围内使用的便携式电话终端，最早是由美国贝尔实验室在1940年制造的战地移动电话机发展而来。'],['智能', '智能，是智力和能力的总称，也有不少思想家把二者结合起来作为一个整体看待。'],['游戏', '按游戏的载体区分，游戏可分为电子游戏和非电子游戏，游戏种类还有团体性游戏，桌面游戏以及野外生存游戏等。'],['电竞', '电子竞技（Electronic Sports），是电子游戏比赛达到“竞技”层面的体育项目。电子竞技就是利用电子设备作为运动器械进行的、人与人之间的智力和体力结合的比拼。'],['旅游', '旅游是结合自己的喜好，主动挖掘尚未熟知的目的地，获得更独特的体验。旅游是一种情绪消费，远离居住地的旅游愈发成为人们舒缓心境、重获力量的重要目的。'],['文化', '文化，广义指人类在社会实践过程中所获得的物质、精神的生产能力和创造的物质、精神财富的总和，狭义指精神生产能力和精神产品，包括一切社会意识形式'],['娱乐', '现代娱乐可被看作是一种通过表现喜怒哀乐或自己和他人的技巧而给予受者喜悦、放松感觉的形式。很显然，这种定义是广泛的，它包含了悲喜剧、各种比赛和游戏、音乐舞蹈表演和欣赏等等。'],['影视', '影视是以拷贝、磁带、胶片、存储器等为载体，以银幕、屏幕放映为目的，从而实现视觉与听觉综合观赏的艺术形式，是现代艺术的综合形态，包含了电影、电视剧、节目、动画等内容。'],['音乐', '在最一般的形式中，将音乐描述为一种艺术形式或文化活动，包括音乐作品的创作（歌曲、曲调、交响曲等），表演，对音乐的评价，对音乐历史的研究以及音乐教学。'],['汽车', '由动力驱动，具有4个或4个以上车轮的非轨道承载的车辆，主要用于：载运人员和（或）货物；牵引载运人员和（或）货物的车辆；特殊用途。'],['教育', '教育（Education）狭义上指专门组织的学校教育；广义上指影响人的身心发展的社会实践活动。拉丁语educare是西方“教育”一词的来源，意思是“引出”。'],['留学', '留学，旧称留洋，一般是指一个人去母国以外的国家接受各类教育，时间可以为短期或长期（从几个星期到几年）。这些学生被称为留学生。'],['高考', '普通高等学校招生全国统一考试（Nationwide Unified Examination for Admissions to General Universities and Colleges），简称“高考”，是合格的高中毕业生或具有同等学力的考生参加的选拔性考试。'],['体育', '体育（physical education，缩写PE或P.E.），是一种复杂的社会文化现象，它是一种以身体与智力活动为基本手段，根据人体生长发育、技能形成和机能提高等规律，达到促进全面发育'],['时政', '当代的政治情况、政治措施,主要和政府政策相关'],['军事','军事（Military） [1] ，即军队事务，古称军务，是与一个国家及政权的国防之武装力量有关的学问及事务。有人认为，军事为政治的一部分，但在中国古代，军、政是分开的。比较正式的说法为，军事是一种政治延续。'],['国际', '国际（International）是一个非常常见的政治用语。它的直接意思是“各个国家之间的”。国际这个词是一个在近代产生的比较新的政治名词'],['太空','星座，是指占星学中必不可少的组成部分之一，亦指天上一群群的恒星组合。自从古代以来，人类便把三五成群的恒星与他们神话中的人物或器具联系起来，称之为“星座”。'],['时尚', '时尚，汉语词语，拼音是shí shàng，指符合潮流的、入时的；流行的风尚；当时的风气和习惯。'],['天气', '天气（weather）是指某一个地区距离地表较近的大气层在短时间内的具体状态。而天气现象则是指发生在大气中的各种自然现象，即某瞬时内大气中各种气象要素（如气温、气压、湿度、风、云、雾、雨、闪、雪、霜、雷、雹、霾等）空间分布的综合表现。'],['自然灾害', '自然灾害（Natural disasters）是指给人类生存带来危害或损害人类生活环境的自然现象。']]


result = {"code": 200, "msg": "Success", "type": "", "data": ""}
if torch.cuda.is_available():
		ner = Taskflow("ner", device_id=0)
else:
		ner = Taskflow("ner", device_id=-1)

def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()

@app.get("/test")
async def test():
    print("------------------")
#API_DIR接口路径，METHOD调用方法
@app.post("/")
async def API_service(request: Request):
	try:
		json_post_raw = await request.json()
		json_post = json.dumps(json_post_raw)
		get_Data = json.loads(json_post)
		content = get_Data.get('content')
		content = content.replace("\"", "").replace("\'", "")
		goal = int(get_Data.get('type'))
		summary =  get_textrank4zh_summarization_str(content)
		## summary
		if goal == 1:
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "文本摘要"
			result["data"] = summary
		## segmentation
		elif goal == 2:
			segmentation = word_segmentation(content)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "文本分词"
			result["data"] = segmentation
		## sensitive word filter
		elif goal == 3:
			sensitive = filter_sensitive(content)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "敏感词过滤"
			result["data"] = sensitive
		## classifier
		elif goal == 4:
			# classifier = classification.classfier_predict(content)
			request = "分类任务：　\n" + summary + "\n 选项：天气，游戏，财经，旅游，科技，娱乐，汽车，教育，体育，时政，军事，国际，星座，时尚，其他"
			classifier = clueAI.answer(request)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "文本分类"
			result["data"] = classifier
		## key word extraction
		elif goal == 5:
			keyword = get_textrank4zh_keywords(content)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "关键词抽取"
			result["data"] = keyword
		## ner
		elif goal == 6:
			ans = ner_exec(content, ner)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "实体识别"
			result["data"] = ans
		elif goal == 7:
			multi_classifier = multiTag.get_tags(content, tags)
			result["code"] = 200
			result["msg"] = "Success"
			result["type"] = "文本聚类"
			result["data"] = multi_classifier
		else:
			result["code"] = 400
			result["msg"] = "Fail: Wrong type number!"
		return result	
		
	except Exception as e:
		print(e)
		result["code"] = 400
		result["msg"] = "Fail"
		return result
 
if __name__ == "__main__":
    uvicorn.run(app='run:app', host='0.0.0.0', port=10002,workers=4)
    # uvicorn.run(app='run:app', host='0.0.0.0', port=10011,workers=4)
