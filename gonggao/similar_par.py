"""
文本相似度模型测试
方法封装
"""
# -*- coding: utf-8 -*-
from tqdm import tqdm
from paddlenlp import Taskflow
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

similarity = Taskflow("text_similarity")
from sentence_transformers import SentenceTransformer, util
path1 = "/home/albay/fl_test/"
clueAI_path = path1+"data/model/clueAI"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = T5Tokenizer.from_pretrained(clueAI_path)
model_clueAI = T5ForConditionalGeneration.from_pretrained(clueAI_path).to(device)
model = SentenceTransformer(path1+"data/model/xcoa-sbert-base-chinese-nli")
# print("加载----------------------")


def preprocess(text):
  return text.replace("\n", "_")

def postprocess(text):
  return text.replace("_", "\n")

def clueAI_output_change(input:str) -> str:
    # result_list = ["现场投标","网上投标"]
    if input == "线上":
        return "网上投标"
    else:
        return "现场投标"
    

def answer(text:str, sample=False, top_p = 0.8):
    """
    官方提供回答方法 
    """
    text = preprocess(text)
    encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt").to(device) 
    if not sample:
        out = model_clueAI.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=128, num_beams=4, length_penalty=0.6)
    else:
        out = model_clueAI.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=64, do_sample=True, top_p=top_p)
    out_text = tokenizer.batch_decode(out["sequences"], skip_special_tokens = True)
    return postprocess(out_text[0])

def clueAI_input_change(input:str)->str:
    """
    clueAI问答式输入转换
    """
    return "阅读理解\n%s\n问题：这是什么地址\n选项：线上，线下\n答案"%input
def tb_method_determin(input:str):
    """
    集成clueAI对投标方式进行判断
    """
    #1.根据关键词进行判断
    # 定义关键词
    keywords = ["在线","网站","系统","交易中心","客户端","平台"]#TODO 需要挖掘补充 上线挖掘
    for item in keywords:
        if item in input:
            return "网上投标"
    return clueAI_output_change(answer(clueAI_input_change(input=input)))

def read_keys(keys_path:str)->list:
    result = list()
    with open(keys_path,"r", encoding="utf-8")as f:
        data = f.readlines()
        for item in data:
            # result.append(item.replace("\n",""))
            result.append(item.split()[0])
    return result

def make_similar_par(pre_vocab, key_list)->list:
    """
    一对多的转换情感分析 输入 的格式
    [[pre_vocab,key_list[0]],[pre_vocab,key_list[1],...,[pre_vocab,key_list[n]]
    """
    result = list()
    for item in key_list:
        result.append([pre_vocab, item])
    return result
MIN_SIMILARY = 0.1
def get_similary_key(data):
    result = similarity(data)
    #对similary进行排序返回相似度最大的关键字 设置一个阈值
    # 最大的如果没超过也不算匹配上并且提示出现新的关键字
    max_similarity = 0
    max_text2 = ''
    max_text1 = ''
    for item in result:
        if item['similarity'] > max_similarity:
            max_similarity = item["similarity"]
            max_text2 = item['text2']
            max_text1 = item['text1']
    if max_similarity < MIN_SIMILARY:
        return None
    return max_text2, max_similarity
def unify_vocab(pre_list: list, key_list_path: str) -> list:
    """
    实现 相似度 映射 利用 paddle-similar模型 该模型不提供微调接口
    """
    # print(pre_list)
    result = list()
    key_list = read_keys(key_list_path)# 获取关键词的list
    for item in pre_list:
       # if item is '':
        #    continue
        data = make_similar_par(pre_vocab=item, key_list=key_list)
        # 预测
        max_text_similar = get_similary_key(data)
        if max_text_similar is not None:
            # continue
            # 去掉已经识别到的关键字
            result.append(max_text_similar[0])
            key_list.remove(max_text_similar[0])
        if len(key_list) == 0:
            return result
    result = list(set(result))
    return result

def tb_method_determineBybid_file_place_or_tb_method(input_text:str)->str:
    """
    根据投标地址
        input_text
        判断
            tb_method   
                是 现场投标 还是 网上投标
    
    Args:
        input_text (str): input_text
    Returns:
        _type_: 现场投标/网上投标
    """
    # 1.定义返回值
    result = ""
    # 2. 定义投标方式
    tb_fangshi_list = ["现场投标", "网上投标"]
    tb_fangshi_relation_list=["线下","线上"]
    # 4.批量 相似度 构造 输入数据
    data=[ [input_text, item] for item in tb_fangshi_relation_list]
    # 5.利用模型进行批量相似度计算并且获取最大相似度的tb_fangshi
    result = max(similarity(data), key = lambda x:x['similarity'])["text2"]
    return result

def bm_fangshi2bm_fangshi_2(input_text:str)->str:
    """
    根据报名地址input_text判断tb_fangshi  是 网上报名 现场报名 邮寄报名 邮件报名
    
    Args:
        input_text (str): input_text
    Returns:
        _type_: 现场投标/网上投标
    """
    # 1.定义返回值
    result = ""
    # 2. 定义投标方式
    tb_fangshi_list = ["注册报名", "现场报名","邮寄报名","邮件报名"]
    # 4.批量 相似度 构造 输入数据
    data=[ [input_text, item] for item in tb_fangshi_list]
    # 5.利用模型进行批量相似度计算并且获取最大相似度的tb_fangshi
    result = max(similarity(data), key = lambda x:x['similarity'])["text2"]
    return result

def bm_fangshi2bm_fangshi(input_text:str)->str:
    """
    同
    tb_method_determineBybid_file_place_or_tb_method()
    模型不一样
    一样
    """
    result = ""
    tb_fangshi_list = ["注册报名", "现场报名","邮寄报名","邮件报名"]
    input_text_list= [input_text] * len(tb_fangshi_list)
    
    #Compute embedding for both lists
    embeddings1 = model.encode(input_text_list, convert_to_tensor=True)
    embeddings2 = model.encode(tb_fangshi_list, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    cosine_scores_list = cosine_scores[0].tolist()
    max_index = cosine_scores_list.index(max(cosine_scores_list))
    return tb_fangshi_list[max_index]


if __name__ == "__main__" :
    path1 = "/home/albay/fl_test/test_update_2/"
    reg_condition_keys_path = path1+ "data/0606_reg_condition_keys.txt"
    credentials_condition_keys_path = path1+ "data/0606_credentials_vocab_keys.txt"
    
    result = unify_vocab(["法人证书", "什么法人授权证书"], reg_condition_keys_path)
    print("---",result)
    pass
