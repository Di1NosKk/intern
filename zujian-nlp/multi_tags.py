from sentence_transformers import SentenceTransformer, util
import numpy as np
from textrank4zh import TextRank4Keyword, TextRank4Sentence, Segmentation
import os 

class Tag():
    def __init__(self):
        script_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(script_path)
        self.model_m3e = SentenceTransformer(this_dir + '/moka-ai/m3e-base')
        
    def get_textrank4zh_summarization_str(self, content):
        """
        获取文本摘要，返回的是string
        :param contents: string
        :return: string
        """
        # 定义返回前5个文本摘要
        topK = 1
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=content, lower=True, source='all_filters')
        result_topK = tr4s.get_key_sentences(num=topK)

        temp = []
        for item in result_topK:
            sent = item['sentence']
            temp.append(sent)

        return '。'.join(temp)
    
    def select_large_values(self, dictionary, threshold):
        # Calculate mean and standard deviation of the values
        values = list(dictionary.values())
        mean = np.mean(values)
        std = np.std(values)

        # Calculate z-score for each value
        z_scores = [(value - mean) / std for value in values]

        # Create a new dictionary to store the selected key-value pairs
        selected_cases = {}

        # Iterate over the dictionary and select cases with z-score exceeding the threshold
        for key, z_score in zip(dictionary.keys(), z_scores):
            if z_score > threshold:
                selected_cases[key] = dictionary[key]

        return selected_cases


    def get_tags(self, text, tags):
        
        # res = self.get_textrank4zh_summarization_str(text)
        # print(res)
        # 检查text包含哪些tags
        res = text
        result = []
        s_dict = {}
        num = 0
        for tag in tags:
            embeddings = self.model_m3e.encode([tag[0], res])
            s = util.cos_sim(embeddings[0], embeddings[1]).tolist()[0][0]
            s_dict[tag[0]] = s
        # sort_s = dict([value, key] for key,value in s_dict.items())
        # print(sorted(sort_s.items()))
            
        result = self.select_large_values(s_dict, 1.9)

        return list(result.keys()) if result else ["其它"]
