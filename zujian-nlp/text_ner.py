from paddlenlp import Taskflow
import os

def merge_ner_results(ner_results):  
    merged_results = {}
    for entities, category in ner_results: 
        if len(entities) == 1:
            continue 
        if category == '人物类_实体' or category == '人物类_概念':  
            category = '人物类'  
        elif "作品类" in category:
            category = '作品类'
        elif "组织机构类" in category:
            if "企事业单位" in category:
                category = "公司"
            elif "国家机关" in category:
                category = "政府"
            else:
                category = "组织机构类"
        elif "物体类" in category:
            category = "物体类"
        elif "文化类" in category:
            category = "文化类"
        elif "生物类" in category:
            category = "生物类"
        elif "场所类" in category:
            category = "场所类"
        elif category == "世界地区类":
            category = "地点"
        elif "饮食类" in category:
            category = "饮食类"
        elif "品牌名" in category:
            category = "品牌名"
        elif "药物类" in category:
            category = "药物类"
        elif "信息资料" in category:
            category = "信息资料"
        elif category == "医学术语类" or category == "术语类_生物体" or category == "疾病损伤类" or category == "疾病损伤类_植物病虫害":
            category = "生物医学"
        elif category == "时间类" or category == "时间类_特殊日":
             category = "时间类"
        elif category =="术语类" or category == "术语类_符号指标类":
            category = "术语类"
        elif category == "词汇用语":
            category = "词汇用语"
        else:
            # category = "其它"
            continue
        merged_results[entities] = category
    return merged_results
def ner_exec(content, ner):
    # script_path = os.path.abspath(__file__)
    # this_dir = os.path.dirname(script_path)
    # path = this_dir + "/models/ner/wordtag_v1.3"
    # ner = Taskflow("ner", device_id=device, task_path=path)
    # ner = Taskflow("ner", device_id=device)
    result = ner(content)
    result = merge_ner_results(result)
    return result
