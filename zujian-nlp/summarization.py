
from textrank4zh import TextRank4Keyword, TextRank4Sentence, Segmentation
import os
import sys
from harvesttext import HarvestText

def get_textrank4zh_summarization_str(content):
    """
    获取文本摘要，返回的是string
    :param contents: string
    :return: string
    """
    # 定义返回前5个文本摘要
    topK = 5
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=content, lower=True, source='all_filters')
    result_topK = tr4s.get_key_sentences(num=topK)

    temp = []
    for item in result_topK:
        sent = item['sentence']
        temp.append(sent)

    return '。'.join(temp)

def get_textrank4zh_keywords(contents):
    """
    获取文本关键字
    :param contents: string
    :return: dict of list [{x},{x}]
    """
    """
    # 定义返回前10个关键词
    topK = 10
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=contents, lower=True)

    # logger.info('使用textrank4zh提取关键词，默认提取10个')
    # print('摘要：')
    # for item in tr4w.get_keywords(10, word_min_len=1):
    #     print(item.word, item.weight)
    result_topK = tr4w.get_keywords(topK, word_min_len=1)

    print(result_topK)
    result = []
    # 封装成指定字典格式
    for i, wp in enumerate(result_topK):
        result.append(wp['word'])
    """
    # 比textrank准确性高
    ht = HarvestText()
    result = ht.extract_keywords(contents, 10, method="jieba_tfidf")
    return result