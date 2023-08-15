# paddle 分词
# from paddlenlp import Taskflow
# seg = Taskflow("word_segmentation")

# def word_segmentation(content):

#     return seg(content)


# jieba分词
import jieba
import re
import os
def word_segmentation(content):
    with open(os.path.join(os.path.abspath("."), "stop_words.txt")) as f:
        stop_words = f.read()
    words=jieba.lcut(content) #0. 分词过滤
    fwords = [word for word in words if len(word.strip())> 1]  # 1.单字过滤
    f2words=[word for word in fwords if word not in stop_words] # 2.停用词过滤
    f3words = [word for word in f2words if not re.match(r'\d+年|\d+月|\d+日|\d+点|\d+分|\d+时|\d+秒', word)] #3. 时间过滤
    f4words=list(set(f3words)) # 4.重复元素过滤
    f5words=[word for word in f4words if not re.match(r'\d+', word)]  #5. 数字元素剔除
    return f5words
    