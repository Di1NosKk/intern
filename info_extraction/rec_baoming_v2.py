import os
import jionlp
import re
import datetime
import jieba
from paddlenlp import Taskflow
import paddlenlp
import json
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from pprint import pprint
from tqdm import tqdm

"""recognize needed info from short sentences"""
account_name = ['账户公司名称', '收款单位', '开户单位']
schema1 = account_name # Define the schema for entity extraction
ie1 = Taskflow('information_extraction', schema=schema1,)
schema2 = ['开户银行']
ie2 = Taskflow('information_extraction', schema=schema2)
schema3 = ['银行账号']
ie3 = Taskflow('information_extraction', schema=schema3)

account = ['银行账户：','账户名称：','账户名称:','收款人全称：','开户名：','开户名称：','收款单位：','收款名称：','单位名称：','开户单位名称：','开户单位：','公司名称：','户名：','收款人：','账户信息：','单位名称:']
bank = ['开户行：', '开户银行：', '保证金交纳银行：','开户银行名称：', '开户行名称：', '开户银行（']
bank_account = ['银行账号：', '账号：', '开户账号：']

contents=[]
id_bid = []
new_contents = []

def main():
    with open(os.path.dirname(os.path.abspath("__file__"))+"/data/20231515_data.txt") as f_in:
        data = f_in.readlines()[1:]
        for line in tqdm(data):
            try:
                if line.split("\t")[1]!="NULL":
                    id_bid.append(line.split("\t")[0])
                    contents.append(line.split("\t")[1])
            except(IndexError) as e:
                pass

    """clear context"""
    for i in range(len(contents)):
        contents[i] = clear_info(contents[i])

    """new content with required info"""
    for i in range(len(contents)):
        lst1 = []
        for ij in range(len(bank_account)): 
            index1 = contents[i].rfind(bank_account[ij])
            if index1 != -1: 
                lst1.append(index1)
        for ik in range(len(bank)):
            index2 = contents[i].rfind(bank[ik])
            if index2 != -1:
                lst1.append(index2)
        for il in range(len(account)):
            index3 = contents[i].rfind(account[il])
            if index3 != -1:
                lst1.append(index3)

        if lst1 != []:
            new_contents.append(contents[i][min(lst1):])
        else:
            new_contents.append(0)

    """extract info"""
    ans = []
    update = 0
    try:
        for content in new_contents:
            update += 1 
            print("第{}份".format(update))
            print()
            res = get_info(content)
            ans.append(res)
    except Exception as e: 
        print("Error: ", e)

    with open(os.path.dirname(os.path.abspath("__file__"))+"/20231515_data_output_2.txt", "w") as f_out:
        for a in ans: 
            f_out.write(str(a) + '\n')

def clear_info(content):
    content=jionlp.remove_html_tag(content)
    pattern1 = re.compile(r'\{[^{}]*?\}')
    pattern2 = re.compile(r'\<[^<>]*?\>')
    content =  pattern2.sub('', content)
    content = pattern1.sub('', content)
    content = content.replace("\xa02","").replace("\xa01","").replace("\xa0","").replace(" ","").replace(";","").replace("\u3000","").replace("&nbsp","").replace("■","").replace("_","").replace("\\t","").replace("\n","").split("\\n")

    content=[item for item in content if item !='' or "notice" not in item or "font" not in item]
    return "".join(content)
        
def clear_paddle_IE(paddle_data) -> dict:
    """清洗paddlepaddle解析文件
    经多层嵌套的list 简单保留name:text
    """
    result = dict()
    for item in paddle_data[0]:
        result[item] = paddle_data[0].get(item)[0]["text"]
    return result

def get_info(content): 
    res = {"bank_name":"", "account_name":"", "account_number":""}

    if content != 0:

        result1 = clear_paddle_IE(ie1(content))
        result2 = clear_paddle_IE(ie2(content))
        result3 = clear_paddle_IE(ie3(content))

        result1.get('账户公司名称') 
        result1.get('收款单位') 
        result1.get('开户单位')
        result2.get('开户银行')
        result3.get('开户账号')

        res["bank_name"] = result2.get('开户银行')

        if result1.get('账户公司名称') is not None:
            res["account_name"] = result1.get('账户公司名称')
        elif result1.get('收款单位') is not None: 
            res["account_name"] = result1.get('收款单位') 
        elif result1.get('开户单位') is not None: 
            res["account_name"] = result1.get('开户单位')
        else : 
            res["account_name"] = ""

        res["account_number"] = result3.get('银行账号')

        if res["bank_name"] is None:
            res["开户银行名称"] = ""
        if res["account_name"] is None: 
            res["account_name"] = ""
        if res["account_number"] is None:
            res["account_number"] = ""
    else:
        res["bank_name"] = ""
        res["account_name"] = ""                
        res["account_number"] = ""

    return res

if __name__ == "__main__":
    main()
