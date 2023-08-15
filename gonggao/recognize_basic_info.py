import os
import jionlp
import re
import jieba
from paddlenlp import Taskflow
import paddlenlp
import json
import clueClassify

clueAI = clueClassify.ClueAI()

def clear_baoming_info(content: str) -> str:
    content = jionlp.remove_html_tag(content)
    pattern1 = r'\{[^{}]*?\}'
    pattern2 = r'\<[^<>]*?\>'
    content = re.compile(pattern2).sub('', content)
    content = re.compile(pattern1).sub('', content)
    content = content.replace("\xa02", "").replace("\xa01", "").replace("\xa0", "").replace(" ", "").replace(";","").replace(
        "\u3000", "").replace("&nbsp", "").replace("■", "").replace("★", "").replace("_", "").replace("\\t", "").split(
        "\\n")
    content = [item for item in content if item != '' or "notice" not in item or "font" not in item]
    return "".join(content)

def get_basic_info(content):
    result = {"xmbh":""}
    content = clear_baoming_info(content)
    content = content[:300]
    xmbh = ['项目编号','招标编号','外协编号','工程编号']
    lst1 = [content.find(key) for key in xmbh if content.find(key) != -1]

    if lst1 != []:
        xmbh_content = content[min(lst1):min(lst1)+50]
        # print(xmbh_content)
        question_xmbh = "信息抽取：\n" + xmbh_content + "\n问题：项目编号\n答案："
        result["xmbh"] = clueAI.answer(question_xmbh)
    else:
        xmbh_content = content[:100]
        # print(xmbh_content)
        question_xmbh = "信息抽取：\n" + xmbh_content + "\n问题：项目编号\n答案："
        result["xmbh"] = clueAI.answer(question_xmbh)
    if len(result["xmbh"]) > 50:
        result["xmbh"] = ""
    return result
    