from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import torch

class ClueAI():
    def __init__(self):
        script_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(script_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = T5Tokenizer.from_pretrained(this_dir + "/clueAI")
        self.model = T5ForConditionalGeneration.from_pretrained(this_dir + "/clueAI").to(self.device)   

    def preprocess(self, text):
        return text.replace("\n", "_")

    def postprocess(self, text):
        return text.replace("_", "\n")

    def answer(self, text, sample=False, top_p=0.8):
        '''sample：是否抽样。生成任务，可以设置为True;
        top_p：0-1之间，生成的内容越多样'''
        text = self.preprocess(text)
        encoding = self.tokenizer(text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt").to(self.device) 
        if not sample:
            out = self.model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=128, num_beams=4, length_penalty=0.6)
        else:
            out = self.model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=64, do_sample=True, top_p=top_p)
        out_text = self.tokenizer.batch_decode(out["sequences"], skip_special_tokens=True)
        return self.postprocess(out_text[0])
