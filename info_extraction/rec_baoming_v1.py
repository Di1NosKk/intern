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

def get_info(content, i, index, ind): 
    
#     print()
#     print()

    res = {"开户银行名称":"", "开户名称":"", "开户账号":""}

#     print(i)
#     print(index[ind])
    if i == index[ind]: 

        result1 = clear_paddle_IE(ie1(content))
        result2 = clear_paddle_IE(ie2(content))
        result3 = clear_paddle_IE(ie3(content))

        result1.get('账户公司名称') 
        result1.get('收款单位') 
        result1.get('开户单位')
        result2.get('开户银行')
        result3.get('开户账号')

        res["开户银行名称"] = result2.get('开户银行')

        if result1.get('账户公司名称') is not None:
            res["开户名称"] = result1.get('账户公司名称')
        elif result1.get('收款单位') is not None: 
            res["开户名称"] = result1.get('收款单位') 
        elif result1.get('开户单位') is not None: 
            res["开户名称"] = result1.get('开户单位')
        else : 
            res["开户名称"] = ""


        res["开户账号"] = result3.get('银行账号')

#         res["文本"] = contents[i]
#         print(res)
#         print(1)
#         print()

        ind += 1

    else:

        res["开户银行名称"] = ""
        res["开户名称"] = ""                
        res["开户账号"] = ""
#         res["文本"] = contents[i]
#         print(res)
#         print(2)
#         print()
           
    return res, ind

def main():
    
    contents=[]
    id_bid = []
    
    with open(os.path.dirname(os.path.abspath("__file__"))+"/data/20231515_data.txt")as f:
        data = f.readlines()[1:]
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
        
    
    # """search keyword while testing"""
    # for i in range(len(contents)):
    #     if "0720622011015200005459" in contents[i]:
    #         print(i)
    #         print(contents[12])
    
    account = ['银行账户','账户名称', '收款人全称', '开户名', '收款单位','收款名称', '开户单位名称', '开户单位']
    bank = ['开户行', '开户银行', '保证金交纳银行']
    bank_account = ['银行账号', '账号', '开户账号']
    
    """filter info"""
    index = []
    for i in range(len(contents)):
        for acc in bank_account: 
            if acc in contents[i]:
                index.append(i)
#     print(index)

    """new list with index containing bank_account"""
    lst = []
    for el in index:
        if lst.count(el) < 1:
            lst.append(el)

    """extract info"""
    ans = []
    ind = 0
    try:
        for i in range(len(contents)):
            print("第{}份".format(i))
            print()
            
#             if(i == 38):
#                 break
            res, ind = get_info(contents[i], i, lst, ind)
            ans.append(res)
    except Exception as e: 
        print("Error: ", e)
        
    with open(os.path.dirname(os.path.abspath("__file__"))+"/20231515_data_output2.txt", "w") as f_out:
        for a in ans: 
            f_out.write(str(a) + '\n')
    print(ans)

if __name__ == "__main__":
    """recognize needed info from short sentences"""
    account_name = ['账户公司名称', '收款单位', '开户单位']
    schema1 = account_name # Define the schema for entity extraction
    ie1 = Taskflow('information_extraction', schema=schema1,)
    schema2 = "开户银行"
    ie2 = Taskflow('information_extraction', schema=schema2)
    schema3 = "银行账号"
    ie3 = Taskflow('information_extraction', schema=schema3)
    main()